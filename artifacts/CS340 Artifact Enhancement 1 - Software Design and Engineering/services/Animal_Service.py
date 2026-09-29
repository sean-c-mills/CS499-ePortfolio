# Imports Pandas for working with animal records as DataFrames
import pandas as pd

# Prepares MongoDB animal records for use by the dashboard
def prepare_animal_dataframe(records):

    # Converts the MongoDB records into a DataFrame
    dataframe = pd.DataFrame.from_records(
        records
    )

    # Returns the empty DataFrame if no records were found
    if dataframe.empty:
        return dataframe

    # Removes the MongoDB ObjectId because it isn't needed in the table
    if "_id" in dataframe.columns:
        dataframe.drop(
            columns=["_id"],
            inplace=True
        )

    # Removes duplicate records when an animal ID is available
    if "animal_id" in dataframe.columns:
        dataframe.drop_duplicates(
            subset=["animal_id"],
            inplace=True
        )

    # Moves the animal name beside the animal type for easier viewing
    if (
        "name" in dataframe.columns
        and "animal_type" in dataframe.columns
    ):
        name_column = dataframe.pop(
            "name"
        )

        dataframe.insert(
            dataframe.columns.get_loc(
                "animal_type"
            ) + 1,
            "name",
            name_column
        )

    # Returns the prepared animal records
    return dataframe

# Retrieves shelter animals based on the selected browsing category
def get_animals_by_type(
    shelter,
    animal_type="all"
):

    # Retrieves all animal records when no specific type is selected
    if (
        animal_type is None
        or animal_type == "all"
    ):
        query = {}

    # Finds rabbits that are stored as Other in the original data
    elif animal_type == "Rabbit":
        query = {
            "animal_type": "Other",
            "breed": {
                "$regex": "Rabbit",
                "$options": "i"
            }
        }

    # Finds livestock and non-rabbit animals stored as Other
    elif animal_type == "Other":
        query = {
            "$or": [
                {
                    "animal_type": "Livestock"
                },
                {
                    "$and": [
                        {
                            "animal_type": "Other"
                        },
                        {
                            "breed": {
                                "$not": {
                                    "$regex": "Rabbit",
                                    "$options": "i"
                                }
                            }
                        }
                    ]
                }
            ]
        }

    # Uses the selected animal type for standard categories
    else:
        query = {
            "animal_type": animal_type
        }

    # Retrieves animal records that match the MongoDB query
    records = shelter.read(
        query
    )

    # Prepares the records for display in the dashboard
    dataframe = prepare_animal_dataframe(
        records
    )

    # Displays rabbits as Rabbit without changing the MongoDB records
    if (
        animal_type == "Rabbit"
        and not dataframe.empty
        and "animal_type" in dataframe.columns
    ):
        dataframe["animal_type"] = "Rabbit"

    # Returns the completed DataFrame to the dashboard
    return dataframe