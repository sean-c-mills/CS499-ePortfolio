# Imports tools used to locate project files and measure execution time
from pathlib import Path
import heapq
import re
import sys
import time

# Imports Pandas for loading and preparing benchmark data
import pandas as pd

# Finds the project root so service modules can be imported from the tests folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Adds the project root to the Python import path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Imports the rescue profiles used by the dashboard
from services.Rescue_Profiles import get_default_profiles

# Imports the ranking functions used by the dashboard
from services.Rescue_Ranking_Service import (
    calculate_suitability_score,
    rank_candidates_full_sort,
    rank_candidates_top_k
)

# Defines the files used by the benchmark
DATA_FILE = PROJECT_ROOT / "data" / "aac_shelter_outcomes.csv"
RESULTS_FILE = PROJECT_ROOT / "tests" / "Rescue_Ranking_Benchmark_Results.csv"

# Uses Water Rescue as the consistent profile for performance testing
BENCHMARK_PROFILE = "water"

# Uses the dashboard's default number of ranked candidates
TOP_K_RESULTS = 10

# Sets the dataset sizes used during performance testing
BENCHMARK_SIZES = [
    100,
    500,
    1000,
    5000,
    10000
]

# Repeats the complete ranking tests several times
END_TO_END_REPEATS = 5

# Repeats the faster selection-only tests more times for stable measurements
SELECTION_REPEATS = 100

# Loads animal records from the original shelter dataset
def load_animal_data():

    # Reads the shelter CSV into a DataFrame
    dataframe = pd.read_csv(DATA_FILE)

    # Converts the age field into numeric values for filtering and scoring
    dataframe["age_upon_outcome_in_weeks"] = pd.to_numeric(
        dataframe["age_upon_outcome_in_weeks"],
        errors="coerce"
    )

    return dataframe

# Retrieves animals that meet the selected rescue requirements
def get_eligible_animals(dataframe, profile):

    # Creates a regular expression from the preferred rescue breeds
    breed_pattern = "|".join(
        re.escape(breed) for breed in profile["breeds"]
    )

    # Applies the same main eligibility requirements used by the rescue search
    eligible_animals = dataframe[
        (dataframe["animal_type"] == "Dog")
        & (
            dataframe["breed"].str.contains(
                breed_pattern,
                case=False,
                na=False,
                regex=True
            )
        )
        & (dataframe["sex_upon_outcome"] == profile["sex"])
        & (
            dataframe["age_upon_outcome_in_weeks"].between(
                profile["min_age_weeks"],
                profile["max_age_weeks"]
            )
        )
    ].copy()

    # Resets the index so each candidate has a consistent position
    return eligible_animals.reset_index(drop=True)

# Creates a larger dataset while preserving the original candidate records
def build_benchmark_dataset(eligible_animals, size):

    # Stops if no eligible animals are available for testing
    if eligible_animals.empty:
        raise ValueError(
            "No eligible rescue candidates are available for benchmarking."
        )

    # Calculates how many times the candidate records need to be repeated
    repeat_count = (
        size + len(eligible_animals) - 1
    ) // len(eligible_animals)

    # Repeats the same eligible records to create a controlled larger dataset
    benchmark_data = pd.concat(
        [eligible_animals] * repeat_count,
        ignore_index=True
    ).head(size).copy()

    # Gives repeated records unique IDs so ranked results can be compared
    benchmark_data["animal_id"] = [
        f"{animal_id}_benchmark_{index}"
        for index, animal_id in enumerate(
            benchmark_data["animal_id"].fillna("unknown")
        )
    ]

    return benchmark_data

# Creates scored candidates before the selection-only benchmark begins
def build_scored_candidates(dataframe, profile):

    # Stores the score, original position, and animal ID for each candidate
    scored_candidates = []

    # Calculates each suitability score only once
    for position, (_, row) in enumerate(dataframe.iterrows()):

        candidate = row.to_dict()
        score = calculate_suitability_score(candidate, profile)

        scored_candidates.append(
            (
                score,
                position,
                candidate["animal_id"]
            )
        )

    return scored_candidates

# Selects the top-k candidates by fully sorting all scored candidates
def select_top_k_full_sort(scored_candidates, k):

    # Sorts every candidate before keeping the strongest k results
    ranked_candidates = sorted(
        scored_candidates,
        key=lambda item: (-item[0], item[1])
    )

    # Returns the ranked animal IDs
    return [
        item[2] for item in ranked_candidates[:k]
    ]

# Selects the top-k candidates using a bounded priority queue
def select_top_k_priority_queue(scored_candidates, k):

    # Stores only the strongest k candidates found so far
    priority_queue = []

    # Evaluates each previously scored candidate
    for score, position, animal_id in scored_candidates:

        queue_item = (score, -position, animal_id)

        # Adds candidates until the queue reaches k items
        if len(priority_queue) < k:
            heapq.heappush(priority_queue, queue_item)

        # Replaces the weakest candidate when a stronger one is found
        elif (score, -position) > (
            priority_queue[0][0],
            priority_queue[0][1]
        ):
            heapq.heapreplace(priority_queue, queue_item)

    # Orders the retained candidates from highest score to lowest score
    ranked_candidates = sorted(
        priority_queue,
        key=lambda item: (-item[0], -item[1])
    )

    # Returns the ranked animal IDs
    return [
        item[2] for item in ranked_candidates
    ]

# Measures the average time of a complete ranking method
def measure_end_to_end_time(ranking_function, dataframe, profile):

    elapsed_times = []

    # Repeats the test using the same candidate records
    for _ in range(END_TO_END_REPEATS):

        start_time = time.perf_counter()

        ranking_function(
            dataframe,
            profile,
            k=TOP_K_RESULTS
        )

        end_time = time.perf_counter()
        elapsed_times.append(end_time - start_time)

    # Returns the average execution time in milliseconds
    return (
        sum(elapsed_times) / len(elapsed_times)
    ) * 1000

# Measures only the selection portion of a ranking method
def measure_selection_time(selection_function, scored_candidates):

    elapsed_times = []

    # Repeats the faster selection test for a more stable average
    for _ in range(SELECTION_REPEATS):

        start_time = time.perf_counter()

        selection_function(
            scored_candidates,
            TOP_K_RESULTS
        )

        end_time = time.perf_counter()
        elapsed_times.append(end_time - start_time)

    # Returns the average execution time in milliseconds
    return (
        sum(elapsed_times) / len(elapsed_times)
    ) * 1000

# Checks that the production ranking methods return the same candidates
def compare_end_to_end_results(dataframe, profile):

    # Ranks the candidates using a complete sort
    full_sort_results = rank_candidates_full_sort(
        dataframe,
        profile,
        k=TOP_K_RESULTS
    )

    # Ranks the same candidates using the bounded priority queue
    priority_queue_results = rank_candidates_top_k(
        dataframe,
        profile,
        k=TOP_K_RESULTS
    )

    # Retrieves the ranked animal IDs from each method
    full_sort_ids = full_sort_results["animal_id"].tolist()
    priority_queue_ids = priority_queue_results["animal_id"].tolist()

    return full_sort_ids == priority_queue_ids

# Checks that the isolated selection methods return the same candidates
def compare_selection_results(scored_candidates):

    full_sort_ids = select_top_k_full_sort(
        scored_candidates,
        TOP_K_RESULTS
    )

    priority_queue_ids = select_top_k_priority_queue(
        scored_candidates,
        TOP_K_RESULTS
    )

    return full_sort_ids == priority_queue_ids

# Runs the complete ranking benchmark
def run_benchmark():

    # Loads the default rescue profiles
    profiles = get_default_profiles()

    # Retrieves the profile selected for benchmark testing
    profile = profiles[BENCHMARK_PROFILE]

    # Loads the original animal shelter dataset
    animal_data = load_animal_data()

    # Retrieves animals that meet the selected rescue requirements
    eligible_animals = get_eligible_animals(
        animal_data,
        profile
    )

    # Stores the benchmark results for each dataset size
    benchmark_results = []

    print("Rescue Ranking Performance Benchmark")
    print(f"Profile: {profile['label']}")
    print(f"Original eligible animals: {len(eligible_animals)}")
    print(f"Top-k value: {TOP_K_RESULTS}")
    print(f"End-to-end repetitions: {END_TO_END_REPEATS}")
    print(f"Selection-only repetitions: {SELECTION_REPEATS}")
    print()

    # Tests both approaches using increasingly larger datasets
    for size in BENCHMARK_SIZES:

        # Builds the same dataset for both ranking approaches
        benchmark_data = build_benchmark_dataset(
            eligible_animals,
            size
        )

        # Calculates scores once for the isolated selection benchmark
        scored_candidates = build_scored_candidates(
            benchmark_data,
            profile
        )

        # Runs each complete method once before timing
        rank_candidates_full_sort(
            benchmark_data,
            profile,
            k=TOP_K_RESULTS
        )

        rank_candidates_top_k(
            benchmark_data,
            profile,
            k=TOP_K_RESULTS
        )

        # Runs each isolated selection method once before timing
        select_top_k_full_sort(
            scored_candidates,
            TOP_K_RESULTS
        )

        select_top_k_priority_queue(
            scored_candidates,
            TOP_K_RESULTS
        )

        # Confirms the complete methods return the same top-k candidates
        same_end_to_end_results = compare_end_to_end_results(
            benchmark_data,
            profile
        )

        # Confirms the isolated methods return the same top-k candidates
        same_selection_results = compare_selection_results(
            scored_candidates
        )

        # Measures the complete full-sort approach
        full_sort_end_to_end = measure_end_to_end_time(
            rank_candidates_full_sort,
            benchmark_data,
            profile
        )

        # Measures the complete priority-queue approach
        priority_queue_end_to_end = measure_end_to_end_time(
            rank_candidates_top_k,
            benchmark_data,
            profile
        )

        # Measures only the full-sort selection operation
        full_sort_selection = measure_selection_time(
            select_top_k_full_sort,
            scored_candidates
        )

        # Measures only the priority-queue selection operation
        priority_queue_selection = measure_selection_time(
            select_top_k_priority_queue,
            scored_candidates
        )

        # Stores the completed result for this dataset size
        benchmark_results.append(
            {
                "records": size,
                "full_sort_end_to_end_ms": round(
                    full_sort_end_to_end,
                    4
                ),
                "top_k_end_to_end_ms": round(
                    priority_queue_end_to_end,
                    4
                ),
                "full_sort_selection_ms": round(
                    full_sort_selection,
                    4
                ),
                "top_k_selection_ms": round(
                    priority_queue_selection,
                    4
                ),
                "same_end_to_end_results": same_end_to_end_results,
                "same_selection_results": same_selection_results
            }
        )

        # Displays the completed results in the console
        print(f"Records: {size}")
        print("End-to-End Ranking:")
        print(f"  Full sort average: {full_sort_end_to_end:.4f} ms")
        print(
            f"  Top-k priority queue average: "
            f"{priority_queue_end_to_end:.4f} ms"
        )
        print(
            f"  Same top {TOP_K_RESULTS}: "
            f"{same_end_to_end_results}"
        )

        print("Selection Only:")
        print(f"  Full sort average: {full_sort_selection:.4f} ms")
        print(
            f"  Top-k priority queue average: "
            f"{priority_queue_selection:.4f} ms"
        )
        print(
            f"  Same top {TOP_K_RESULTS}: "
            f"{same_selection_results}"
        )
        print()

    # Converts the completed benchmark results into a DataFrame
    results_dataframe = pd.DataFrame(benchmark_results)

    # Saves the benchmark results so they can be reviewed later
    results_dataframe.to_csv(
        RESULTS_FILE,
        index=False
    )

    print("Benchmark complete.")
    print(f"Results saved to: {RESULTS_FILE}")

# Runs the benchmark when this file is executed directly
if __name__ == "__main__":
    run_benchmark()