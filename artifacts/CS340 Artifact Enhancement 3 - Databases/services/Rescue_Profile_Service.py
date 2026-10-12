# Defines the MongoDB collection used to store rescue profiles
RESCUE_PROFILE_COLLECTION = "rescue_profiles"

# Retrieves the rescue-profile collection from MongoDB
def get_profile_collection(shelter):

    return shelter.get_collection(
        RESCUE_PROFILE_COLLECTION
    )

# Retrieves every rescue profile stored in MongoDB
def get_all_profiles(shelter):

    # Retrieves the profiles without exposing MongoDB ObjectIds to the application
    profiles = list(
        get_profile_collection(
            shelter
        ).find(
            {},
            {
                "_id": 0
            }
        ).sort(
            "label",
            1
        )
    )

    return profiles

# Retrieves one rescue profile from MongoDB
def get_profile(
    shelter,
    profile_type
):

    # Searches for the requested rescue profile
    profile = get_profile_collection(
        shelter
    ).find_one(
        {
            "profile_type": profile_type
        },
        {
            "_id": 0
        }
    )

    # Stops when the requested profile isn't stored in the database
    if profile is None:
        raise ValueError(
            f"Unknown rescue profile: {profile_type}"
        )

    return profile

# Creates Dash options from the rescue profiles stored in MongoDB
def get_profile_options(shelter):

    # Converts each database profile into a label and value for Dash
    return [
        {
            "label": profile["label"],
            "value": profile["profile_type"]
        }
        for profile in get_all_profiles(
            shelter
        )
    ]

# Saves a validated rescue profile to MongoDB
def save_profile(
    shelter,
    profile
):

    # Updates an existing profile or creates it when it doesn't exist
    get_profile_collection(
        shelter
    ).update_one(
        {
            "profile_type": profile[
                "profile_type"
            ]
        },
        {
            "$set": profile
        },
        upsert=True
    )

    # Returns the saved profile for use by the application
    return profile

# Deletes a rescue profile from MongoDB
def delete_profile(
    shelter,
    profile_type
):

    # Deletes the profile that matches the selected identifier
    result = get_profile_collection(
        shelter
    ).delete_one(
        {
            "profile_type": profile_type
        }
    )

    # Returns the number of profiles that were deleted
    return result.deleted_count