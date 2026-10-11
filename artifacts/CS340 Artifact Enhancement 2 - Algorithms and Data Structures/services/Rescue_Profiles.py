# Imports deepcopy so profile data can be copied without changing the original values
from copy import deepcopy

# Stores the default requirements for each rescue profile
DEFAULT_RESCUE_PROFILES = {

    # Defines the Water Rescue requirements
    "water": {
        "label": "Water Rescue",

        "breeds": [
            "Labrador Retriever",
            "Chesapeake Bay Retriever",
            "Newfoundland"
        ],

        "sex": "Intact Female",

        "min_age_weeks": 26,
        "max_age_weeks": 156
    },

    # Defines the Mountain or Wilderness Rescue requirements
    "mountain": {
        "label": "Mountain or Wilderness Rescue",

        "breeds": [
            "German Shepherd",
            "Alaskan Malamute",
            "Old English Sheepdog",
            "Siberian Husky",
            "Rottweiler"
        ],

        "sex": "Intact Male",

        "min_age_weeks": 26,
        "max_age_weeks": 156
    },

    # Defines the Disaster or Individual Tracking requirements
    "disaster": {
        "label": "Disaster or Individual Tracking",

        "breeds": [
            "Doberman Pinscher",
            "German Shepherd",
            "Golden Retriever",
            "Bloodhound",
            "Rottweiler"
        ],

        "sex": "Intact Male",

        "min_age_weeks": 20,
        "max_age_weeks": 300
    }
}

# Returns a separate copy of the default rescue profiles
def get_default_profiles():

    # Prevents changes from modifying the original default profiles
    return deepcopy(
        DEFAULT_RESCUE_PROFILES
    )

# Retrieves the selected rescue profile
def get_profile(
    profiles,
    profile_type
):

    # Checks that the requested rescue profile exists
    if profile_type not in profiles:
        raise ValueError(
            f"Unknown rescue profile: {profile_type}"
        )

    # Returns the selected profile
    return profiles[
        profile_type
    ]

# Validates rescue-profile values before they are saved
def validate_profile(
    breeds,
    sex,
    min_age_weeks,
    max_age_weeks
):

    # Removes blank breed values and extra spaces
    cleaned_breeds = [
        breed.strip()
        for breed in breeds
        if breed and breed.strip()
    ]

    # Requires at least one preferred breed
    if not cleaned_breeds:
        raise ValueError(
            "At least one breed must be provided."
        )

    # Requires a sex value
    if not sex or not sex.strip():
        raise ValueError(
            "A sex requirement must be provided."
        )

    # Requires both age values
    if (
        min_age_weeks is None
        or max_age_weeks is None
    ):
        raise ValueError(
            "Both minimum and maximum ages are required."
        )

    # Prevents negative age values
    if (
        min_age_weeks < 0
        or max_age_weeks < 0
    ):
        raise ValueError(
            "Age values cannot be negative."
        )

    # Makes sure the minimum age doesn't exceed the maximum age
    if min_age_weeks > max_age_weeks:
        raise ValueError(
            "Minimum age cannot be greater "
            "than maximum age."
        )

    # Returns the cleaned and validated profile values
    return {
        "breeds": cleaned_breeds,
        "sex": sex.strip(),
        "min_age_weeks": int(
            min_age_weeks
        ),
        "max_age_weeks": int(
            max_age_weeks
        )
    }

# Updates the selected rescue profile with validated values
def update_profile(
    profiles,
    profile_type,
    breeds,
    sex,
    min_age_weeks,
    max_age_weeks
):
    
    # Checks that the requested rescue profile exists
    if profile_type not in profiles:
        raise ValueError(
            f"Unknown rescue profile: {profile_type}"
        )

    # Validates the new profile values before applying them
    validated = validate_profile(
        breeds,
        sex,
        min_age_weeks,
        max_age_weeks
    )

    # Creates a separate copy so the current profile data isn't changed directly
    updated_profiles = deepcopy(
        profiles
    )

    # Updates the preferred breeds
    updated_profiles[
        profile_type
    ]["breeds"] = validated["breeds"]

    # Updates the sex requirement
    updated_profiles[
        profile_type
    ]["sex"] = validated["sex"]

    # Updates the minimum age
    updated_profiles[
        profile_type
    ]["min_age_weeks"] = validated[
        "min_age_weeks"
    ]

    # Updates the maximum age
    updated_profiles[
        profile_type
    ]["max_age_weeks"] = validated[
        "max_age_weeks"
    ]

    # Returns the updated rescue-profile data
    return updated_profiles