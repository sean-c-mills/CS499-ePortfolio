# Imports tools used to measure query performance and save the results
from pathlib import Path
from time import perf_counter
import csv

# Imports the MongoDB data-access class
from data_access.CRUD_Python_Module import AnimalShelter

# Imports the MongoDB connection settings
from data_access.Database_Config import get_database_config

# Imports the function used to retrieve rescue profiles
from services.Rescue_Profile_Service import get_profile

# Imports the function used to build the actual rescue query
from services.Rescue_Service import build_rescue_query

# Defines the MongoDB index being evaluated
INDEX_NAME = "rescue_search_index"

INDEX_FIELDS = [
    ("animal_type", 1),
    ("sex_upon_outcome", 1),
    ("age_upon_outcome_in_weeks", 1)
]

# Defines the existing rescue profiles used during testing
PROFILE_TYPES = [
    "water",
    "mountain",
    "disaster"
]

# Defines how many times each query is timed
TEST_RUNS = 25

# Tests one rescue query and returns its performance information
def test_query(
    database,
    collection,
    query,
    profile_type,
    test_type
):

    # Retrieves MongoDB execution statistics for the query
    explain_result = database.command(
        "explain",
        {
            "find": collection.name,
            "filter": query
        },
        verbosity="executionStats"
    )

    # Retrieves the execution statistics from the explain result
    execution_stats = explain_result[
        "executionStats"
    ]

    # Retrieves the winning MongoDB query plan
    winning_plan = explain_result[
        "queryPlanner"
    ]["winningPlan"]

    # Checks whether MongoDB used an index for the query
    index_used = (
        "IXSCAN"
        in str(winning_plan)
    )

    # Runs the query once before timing to warm up the database
    list(
        collection.find(
            query
        )
    )

    # Starts timing the repeated queries
    start_time = perf_counter()

    for _ in range(TEST_RUNS):
        list(
            collection.find(
                query
            )
        )

    # Stops timing after all query runs are complete
    end_time = perf_counter()

    # Calculates the average time for one query
    average_query_ms = (
        (end_time - start_time)
        / TEST_RUNS
        * 1000
    )

    # Returns the results for the current query
    return {
        "test_type": test_type,
        "profile_type": profile_type,
        "documents_returned": execution_stats[
            "nReturned"
        ],
        "documents_examined": execution_stats[
            "totalDocsExamined"
        ],
        "keys_examined": execution_stats[
            "totalKeysExamined"
        ],
        "execution_time_ms": execution_stats[
            "executionTimeMillis"
        ],
        "average_query_ms": round(
            average_query_ms,
            4
        ),
        "index_used": index_used
    }

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

# Gets the animal collections used by the dashboard
animal_collection = shelter.get_collection(
    "animals"
)

# Stores all of the benchmark results
results = []

# Removes the proposed index if it already exists
if INDEX_NAME in animal_collection.index_information():
    animal_collection.drop_index(
        INDEX_NAME
    )

# Tests each rescue query before adding the proposed index
for profile_type in PROFILE_TYPES:

    # Retrieves the rescue profile from MongoDB
    profile = get_profile(
        shelter,
        profile_type
    )

    # Builds the same query used by the dashboard
    query = build_rescue_query(
        profile
    )

    # Test the query without the proposed index
    result = test_query(
        shelter.database,
        animal_collection,
        query,
        profile_type,
        "Without Index"
    )

    results.append(
        result
    )

    print(
        f"Without Index - {profile_type}: "
        f"{result['documents_examined']} documents examined, "
        f"{result['average_query_ms']} ms average"
    )

# Creates the proposed compound index
animal_collection.create_index(
    INDEX_FIELDS,
    name=INDEX_NAME
)

print(
    f"\nCreated index: {INDEX_NAME}\n"
)

# Tests each rescue query after adding the proposed index
for profile_type in PROFILE_TYPES:

    # Retrieves the rescue profile from MongoDB
    profile = get_profile(
        shelter,
        profile_type
    )

    # Builds the same query used by the dashboard
    query = build_rescue_query(
        profile
    )

    # Tests the query with the proposed index
    result = test_query(
        shelter.database,
        animal_collection,
        query,
        profile_type,
        "With Index"
    )

    results.append(
        result
    )

    print(
        f"With Index - {profile_type}: "
        f"{result['documents_examined']} documents examined, "
        f"{result['keys_examined']} keys examined, "
        f"{result['average_query_ms']} ms average, "
        f"index used: {result['index_used']}"
    )

# Builds the path that is used to save the benchmarks results
results_path = (
    Path(__file__).resolve().parent
    / "Database_Index_Benchmark_Results.csv"
)

# Saves the benchmark results to a CSV file
with open(
    results_path,
    "w",
    newline="",
    encoding="utf-8"
) as results_file:

    writer = csv.DictWriter(
        results_file,
        fieldnames=[
            "test_type",
            "profile_type",
            "documents_returned",
            "documents_examined",
            "keys_examined",
            "execution_time_ms",
            "average_query_ms",
            "index_used"
        ]
    )

    writer.writeheader()
    writer.writerows(
        results
    )

# Displays where the benchmark results were saved
print(
    f"\nBenchmark results saved to: "
    f"{results_path}"
)

# Reminds the user that the index still needs to be evaluated
print(
    "\nBenchmark completed. Please review the saved results "
    "to compare the query performance."
)

# Close the MongoDB connection
shelter.close()