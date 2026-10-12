# Imports tools used to read the data files
from pathlib import Path
import csv
import json

# Imports the MongoDB data-access class
from data_access.CRUD_Python_Module import AnimalShelter

# Imports the MongoDB connection settings
from data_access.Database_Config import get_database_config

# Imports the function used to validate rescue profiles
from services.Rescue_Profiles import validate_profile

# Imports the function used to save rescue profiles in MongoDB
from services.Rescue_Profile_Service import save_profile

# Loads the MongoDB connection settings
database_config = get_database_config()

# Creates the connection to the animal shelter database
shelter = AnimalShelter(
    database_config["username"],
    database_config["password"],
    database_config["host"],
    database_config["port"],
    database_config["database"]
)

# Gets the MongoDB database used by the application
database = shelter.database

# Gets the animal collection used by the dashboard
animal_collection = shelter.get_collection(
    "animals"
)

# Builds the path to the animal data file
animal_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "aac_shelter_outcomes.csv"
)

# Checks whether the animal collection needs to be initialized
animal_count = animal_collection.count_documents(
    {}
)

if animal_count == 0:

    # Stores the animal records that will be added to MongoDB
    animal_records = []

    # Loads the animal records from the CSV file
    with open(
        animal_path,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as animal_file:

        reader = csv.DictReader(
            animal_file
        )

        # Prepares each animal record for MongoDB
        for record in reader:

            # Converts the numeric fields used by rescue searches and maps
            record["age_upon_outcome_in_weeks"] = float(
                record["age_upon_outcome_in_weeks"]
            )

            record["location_lat"] = float(
                record["location_lat"]
            )

            record["location_long"] = float(
                record["location_long"]
            )

            animal_records.append(
                record
            )

    # Adds the animal records when the CSV contains data
    if animal_records:
        animal_collection.insert_many(
            animal_records
        )

    # Displays the number of animal records that were imported
    print(
        f"Imported animal records: "
        f"{len(animal_records)}"
    )

else:

    # Displays that the existing animal records were preserved
    print(
        f"Animal records already in MongoDB: "
        f"{animal_count}"
    )

# Builds the path to the rescue-profile data file
profile_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "rescue_profiles.json"
)

# Loads the rescue profiles from the JSON file
with open(
    profile_path,
    "r",
    encoding="utf-8"
) as profile_file:
    profiles = json.load(
        profile_file
    )

# Validates and saves each rescue profile
for profile in profiles:

    # Validates the current profile before storing it in MongoDB
    validated_profile = validate_profile(
        profile["profile_type"],
        profile["label"],
        profile["breeds"],
        profile["sex"],
        profile["min_age_weeks"],
        profile["max_age_weeks"]
    )

    # Saves the validated profile to the rescue-profile collection
    save_profile(
        shelter,
        validated_profile
    )

    # Displays the name of each profile that is saved
    print(
        f"Saved: {validated_profile['label']}"
    )

# Defines the MongoDB validation rules for rescue profiles
rescue_profile_validator = {
    "$jsonSchema": {

        # Requires each rescue profile to be stored as a document
        "bsonType": "object",

        # Defines the fields that every rescue profile must contain
        "required": [
            "profile_type",
            "label",
            "breeds",
            "sex",
            "min_age_weeks",
            "max_age_weeks"
        ],

        # Defines the expected data types and limits for profile fields
        "properties": {

            # Requires the profile identifier to be stored as text
            "profile_type": {
                "bsonType": "string"
            },

            # Requires the visible profile name to be stored as text
            "label": {
                "bsonType": "string"
            },

            # Requires at least one preferred breed
            "breeds": {
                "bsonType": "array",
                "minItems": 1,

                # Requires each breed in the list to be stored as text
                "items": {
                    "bsonType": "string"
                }
            },

            # Limits the sex requirement to supported values
            "sex": {
                "enum": [
                    "Intact Female",
                    "Intact Male",
                    "Spayed Female",
                    "Neutered Male"
                ]
            },

            # Requires a nonnegative whole number for the minimum age
            "min_age_weeks": {
                "bsonType": "int",
                "minimum": 0
            },

            # Requires a nonnegative whole number for the maximum age
            "max_age_weeks": {
                "bsonType": "int",
                "minimum": 0
            }
        }
    }
}

# Defines the MongoDB validation rules for animal records
animal_validator = {
    "$jsonSchema": {

        # Requires each animal record to be stored as a document
        "bsonType": "object",

        # Defines the fields needed for rescue searches and map display
        "required": [
            "age_upon_outcome_in_weeks",
            "location_lat",
            "location_long"
        ],

        # Defines the expected data types and limits for required fields
        "properties": {

            # Requires the age value to be numeric and nonnegative
            "age_upon_outcome_in_weeks": {
                "bsonType": [
                    "int",
                    "long",
                    "double",
                    "decimal"
                ],
                "minimum": 0
            },

            # Requires latitude to be numeric and within its valid range
            "location_lat": {
                "bsonType": [
                    "int",
                    "long",
                    "double",
                    "decimal"
                ],
                "minimum": -90,
                "maximum": 90
            },

            # Requires longitude to be numeric and within its valid range
            "location_long": {
                "bsonType": [
                    "int",
                    "long",
                    "double",
                    "decimal"
                ],
                "minimum": -180,
                "maximum": 180
            }
        }
    }
}

# Adds the validation rules to the existing rescue-profile collection
database.command({

    # Selects the collection that will be modified
    "collMod": "rescue_profiles",

    # Applies the rescue-profile validation rules
    "validator": rescue_profile_validator,

    # Requires validation for inserts and updates
    "validationLevel": "strict",

    # Rejects documents that do not pass validation
    "validationAction": "error"
})

# Displays confirmation that rescue-profile validation was applied
print(
    "Validation applied to rescue_profiles."
)

# Adds the validation rules to the existing animal collection
database.command({

    # Selects the collection that will be modified
    "collMod": "animals",

    # Applies the animal-record validation rules
    "validator": animal_validator,

    # Requires validation for inserts and updates
    "validationLevel": "strict",

    # Rejects documents that do not pass validation
    "validationAction": "error"
})

# Displays confirmation that animal validation was applied
print(
    "Validation applied to animals."
)

# Creates the compound index selected for rescue searches
animal_collection.create_index(
    [
        ("animal_type", 1),
        ("sex_upon_outcome", 1),
        ("age_upon_outcome_in_weeks", 1)
    ],
    name="rescue_search_index"
)

# Displays confirmation that the rescue-search index is available
print(
    "Rescue search index is available."
)

# Gets the rescue-profile collection
profile_collection = shelter.get_collection(
    "rescue_profiles"
)

# Displays the number of rescue profiles stored in MongoDB
print(
    f"Rescue profiles in MongoDB: "
    f"{profile_collection.count_documents({})}"
)

# Closes the MongoDB connection
shelter.close()

# Displays confirmation that the setup process is complete
print(
    "The database setup has been completed successfully."
)