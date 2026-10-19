# Imports heap tools used to maintain the top-ranked rescue candidates
import heapq

# Imports Pandas for working with rescue candidates as DataFrames
import pandas as pd

# Maximum points available for each part of the suitability score
MAX_AGE_SCORE = 50.0
EXACT_BREED_SCORE = 50.0
PARTIAL_BREED_SCORE = 40.0

# Converts a text value into a consistent format for comparisons
def normalize_text(value):

    # Returns an empty value when the original value is missing
    if value is None or pd.isna(value):
        return ""

    # Removes extra spaces and ignores capitalization
    return str(value).strip().lower()

# Calculates how closely an animal's age matches the rescue age range
def calculate_age_score(animal_age, profile):

    # Returns zero when the animal age isn't available
    if animal_age is None or pd.isna(animal_age):
        return 0.0

    try:
        # Converts the age values into numbers for the calculation
        age = float(animal_age)
        minimum_age = float(profile["min_age_weeks"])
        maximum_age = float(profile["max_age_weeks"])

    except (TypeError, ValueError, KeyError):
        return 0.0

    # Returns zero if the animal is outside the rescue age range
    if age < minimum_age or age > maximum_age:
        return 0.0

    # Gives the full age score when the profile contains one exact age
    if minimum_age == maximum_age:
        return MAX_AGE_SCORE

    # Finds the middle of the acceptable age range
    midpoint = (minimum_age + maximum_age) / 2

    # Finds the distance between the midpoint and either end of the range
    half_range = (maximum_age - minimum_age) / 2

    # Measures how far the animal's age is from the middle of the range
    distance_from_midpoint = abs(age - midpoint)

    # Gives higher scores to ages closer to the middle of the range
    age_score = MAX_AGE_SCORE * (
        1 - (distance_from_midpoint / half_range)
    )

    # Keeps the score between zero and the maximum value
    return round(max(0.0, min(MAX_AGE_SCORE, age_score)), 2)

# Calculates how closely an animal's breed matches the preferred breeds
def calculate_breed_score(animal_breed, profile):

    # Converts the animal breed into a consistent format
    breed = normalize_text(animal_breed)

    # Returns zero when breed information isn't available
    if not breed:
        return 0.0

    # Starts with no breed points
    best_score = 0.0

    # Checks the animal against each preferred breed
    for preferred_breed in profile["breeds"]:

        preferred = normalize_text(preferred_breed)

        # Skips empty breed values
        if not preferred:
            continue

        # Gives the highest score for an exact breed match
        if breed == preferred:
            score = EXACT_BREED_SCORE

        # Gives partial credit when the preferred breed appears in a mixed breed
        elif preferred in breed:
            score = PARTIAL_BREED_SCORE

        # Gives no breed points when the breed doesn't match
        else:
            score = 0.0

        # Keeps the highest breed score
        if score > best_score:
            best_score = score

    # Returns the best breed score found
    return best_score

# Calculates the total suitability score for one rescue candidate
def calculate_suitability_score(animal, profile):

    # Calculates the age portion of the score
    age_score = calculate_age_score(
        animal.get("age_upon_outcome_in_weeks"),
        profile
    )

    # Calculates the breed portion of the score
    breed_score = calculate_breed_score(
        animal.get("breed"),
        profile
    )

    # Combines both portions into one suitability score
    return round(age_score + breed_score, 2)

# Creates a DataFrame containing the ranked rescue candidates
def build_ranked_dataframe(records, source_columns):

    # Keeps the original columns and places the score at the end
    columns = [
        column for column in source_columns
        if column != "suitability_score"
    ]

    columns.append("suitability_score")

    # Creates the completed ranked DataFrame
    return pd.DataFrame(records).reindex(columns=columns)

# Ranks rescue candidates by sorting all eligible animals:
# Time complexity: O(n log n) for sorting n candidates
# Space complexity: O(n) for storing the scored candidates
def rank_candidates_full_sort(dataframe, profile, k=10):

    # Returns an empty ranked DataFrame when there are no candidates
    if dataframe is None or dataframe.empty or k <= 0:

        source_columns = [] if dataframe is None else list(dataframe.columns)

        return build_ranked_dataframe([], source_columns)

    # Stores every scored rescue candidate
    ranked_candidates = []

    # Scores each eligible animal
    for position, (_, row) in enumerate(dataframe.iterrows()):

        # Creates a separate copy of the animal record
        candidate = row.to_dict()

        # Calculates the candidate's suitability score
        score = calculate_suitability_score(candidate, profile)

        # Adds the score to the animal record
        candidate["suitability_score"] = score

        # Stores the score and original position for consistent ordering
        ranked_candidates.append((score, position, candidate))

    # Sorts every candidate from highest score to lowest score
    ranked_candidates.sort(
        key=lambda item: (-item[0], item[1])
    )

    # Keeps only the highest-ranked k candidates
    top_candidates = [
        item[2] for item in ranked_candidates[:k]
    ]

    # Returns the ranked candidates as a DataFrame
    return build_ranked_dataframe(
        top_candidates,
        list(dataframe.columns)
    )

# Ranks rescue candidates using a bounded priority queue:
# Time complexity: O(n log k + k log k) for selecting and ordering the top k
# Space complexity: O(k) for maintaining the bounded priority queue
def rank_candidates_top_k(dataframe, profile, k=10):

    # Returns an empty ranked DataFrame when there are no candidates
    if dataframe is None or dataframe.empty or k <= 0:

        source_columns = [] if dataframe is None else list(dataframe.columns)

        return build_ranked_dataframe([], source_columns)

    # Stores only the highest-scoring k candidates that are found so far
    priority_queue = []

    # Evaluates each eligible animal
    for position, (_, row) in enumerate(dataframe.iterrows()):

        # Creates a separate copy of the animal record
        candidate = row.to_dict()

        # Calculates the candidate's suitability score
        score = calculate_suitability_score(candidate, profile)

        # Adds the score to the animal record
        candidate["suitability_score"] = score

        # Uses the original position to keep tied scores consistent
        queue_item = (score, -position, candidate)

        # Adds candidates until the queue reaches k animals
        if len(priority_queue) < k:
            heapq.heappush(priority_queue, queue_item)

        # Replaces the lowest scoring stored candidate whenever a higher scoring one is found
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

    # Removes the priority-queue values that aren't needed by the dashboard
    top_candidates = [
        item[2] for item in ranked_candidates
    ]

    # Returns the ranked candidates as a DataFrame
    return build_ranked_dataframe(
        top_candidates,
        list(dataframe.columns)
    )