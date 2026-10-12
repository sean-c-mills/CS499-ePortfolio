# Defines the valid sex requirements for rescue profiles
VALID_SEX_VALUES = [
    "Intact Female",
    "Intact Male",
    "Spayed Female",
    "Neutered Male"
]

# Creates a consistent identifier for a rescue profile
def create_profile_type(label):

    # Requires a profile name before creating an identifier
    if not label or not label.strip():
        raise ValueError(
            "A rescue profile name must be provided."
        )

    # Converts the profile name into a lowercase identifier
    profile_type = (
        label.strip()
        .lower()
        .replace(" ", "-")
    )

    # Returns the completed profile identifier
    return profile_type

# Validates rescue-profile values before they are saved
def validate_profile(
    profile_type,
    label,
    breeds,
    sex,
    min_age_weeks,
    max_age_weeks
):

    # Requires a profile identifier
    if not profile_type or not profile_type.strip():
        raise ValueError(
            "A rescue profile type must be provided."
        )

    # Requires a name for the rescue profile
    if not label or not label.strip():
        raise ValueError(
            "A rescue profile name must be provided."
        )

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

    # Requires a valid sex value
    if sex not in VALID_SEX_VALUES:
        raise ValueError(
            "A valid sex requirement must be provided."
        )

    # Requires both age values
    if (
        min_age_weeks is None
        or max_age_weeks is None
    ):
        raise ValueError(
            "Both minimum and maximum ages are required."
        )

    try:
        # Converts the age values into numbers for validation
        minimum_age = float(min_age_weeks)
        maximum_age = float(max_age_weeks)

    except (TypeError, ValueError):
        raise ValueError(
            "Age values must be numeric."
        )

    # Requires whole-number age values
    if (
        not minimum_age.is_integer()
        or not maximum_age.is_integer()
    ):
        raise ValueError(
            "Age values must be whole numbers."
        )

    # Prevents negative age values
    if (
        minimum_age < 0
        or maximum_age < 0
    ):
        raise ValueError(
            "Age values cannot be negative."
        )

    # Makes sure the minimum age doesn't exceed the maximum age
    if minimum_age > maximum_age:
        raise ValueError(
            "Minimum age cannot be greater "
            "than maximum age."
        )

    # Returns the cleaned and validated profile values
    return {
        "profile_type": profile_type.strip(),
        "label": label.strip(),
        "breeds": cleaned_breeds,
        "sex": sex,
        "min_age_weeks": int(minimum_age),
        "max_age_weeks": int(maximum_age)
    }