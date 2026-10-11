# Imports regular expression tools that are used to safely build the breed searches
import re

# Imports the function that is used to prepare animal records for the dashboard
from services.Animal_Service import (
    prepare_animal_dataframe
)

# Builds a MongoDB query from the selected rescue profile
def build_rescue_query(profile):

    # Creates a breed condition for each preferred breed
    breed_conditions = [
        {
            "breed": {
                # Escapes special characters so breed names are treated as text
                "$regex": re.escape(
                    breed
                ),
                "$options": "i"
            }
        }
        for breed in profile["breeds"]
    ]

    # Combines the rescue requirements into one MongoDB query
    return {
        "$and": [

            # Limits rescue candidates to dogs
            {
                "animal_type": "Dog"
            },

            # Matches any breed included in the rescue profile
            {
                "$or": breed_conditions
            },

            # Matches the required sex
            {
                "sex_upon_outcome": profile[
                    "sex"
                ]
            },

            # Matches animals within the required age range
            {
                "age_upon_outcome_in_weeks": {
                    "$gte": profile[
                        "min_age_weeks"
                    ],
                    "$lte": profile[
                        "max_age_weeks"
                    ]
                }
            }
        ]
    }

# Retrieves animals that match the selected rescue profile
def get_rescue_animals(
    shelter,
    profile
):

    # Builds the MongoDB query from the profile requirements
    query = build_rescue_query(
        profile
    )

    # Retrieves animal records that match the query
    records = shelter.read(
        query
    )

    # Prepares the matching records for display in the dashboard
    return prepare_animal_dataframe(
        records
    )