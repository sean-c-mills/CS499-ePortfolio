# Import the Dash callback tools
from dash import Input, Output, State, no_update

# Import the functions used to work with the rescue profiles
from services.Rescue_Profiles import (
    get_default_profiles,
    get_profile,
    update_profile
)

# Register the callbacks used by the rescue-profile configuration page
def register_admin_callbacks(app):

    # Load the selected rescue profile when the profile 
    # type or the stored profile data changes
    @app.callback(
        [
            Output(
                "profile-breeds",
                "value"
            ),

            Output(
                "profile-sex",
                "value"
            ),

            Output(
                "profile-min-age",
                "value"
            ),

            Output(
                "profile-max-age",
                "value"
            )
        ],

        [
            Input(
                "profile-manager-type",
                "value"
            ),

            Input(
                "rescue-profile-store",
                "data"
            )
        ]
    )
    def load_profile_editor(
        profile_type,
        profiles
    ):

        # Load the default profiles if session data is not available
        if profiles is None:
            profiles = get_default_profiles()

        # Get the profile that is selected by the user
        profile = get_profile(
            profiles,
            profile_type
        )

        # Converts the breed list into text for the breed field
        breeds_text = ", ".join(
            profile["breeds"]
        )

        # Returns the profile values to the configuration fields
        return (
            breeds_text,
            profile["sex"],
            profile["min_age_weeks"],
            profile["max_age_weeks"]
        )

    # Saves the profile whenever the user selects the save button
    @app.callback(
        [
            Output(
                "rescue-profile-store",
                "data"
            ),

            Output(
                "profile-save-status",
                "children"
            )
        ],

        Input(
            "save-profile-button",
            "n_clicks"
        ),

        [
            # Reads the current profile data without triggering the callback
            State(
                "rescue-profile-store",
                "data"
            ),

            State(
                "profile-manager-type",
                "value"
            ),

            State(
                "profile-breeds",
                "value"
            ),

            State(
                "profile-sex",
                "value"
            ),

            State(
                "profile-min-age",
                "value"
            ),

            State(
                "profile-max-age",
                "value"
            )
        ],

        # DON'T run the save callback when the page first loads
        prevent_initial_call=True
    )
    def save_rescue_profile(
        n_clicks,
        profiles,
        profile_type,
        breeds_text,
        sex,
        min_age_weeks,
        max_age_weeks
    ):
        # Load the default profiles if the session data isn't available
        if profiles is None:
            profiles = get_default_profiles()

        # Start with an empty breed list
        breeds = []

        # Splits the breed text into individual values
        if breeds_text:
            breeds = [
                breed.strip()
                for breed in breeds_text.split(",")
                if breed.strip()
            ]

        try:
            # Validates the new values and updates the selected profile
            updated_profiles = update_profile(
                profiles,
                profile_type,
                breeds,
                sex,
                min_age_weeks,
                max_age_weeks
            )

            # Get the profile name for the confirmation message
            profile_label = updated_profiles[
                profile_type
            ]["label"]

            # Saves the updated profiles and shows a success message
            return (
                updated_profiles,
                f"{profile_label} was updated successfully."
            )

        except ValueError as error:
            # Keeps the current profile data when the validation fails
            return (
                no_update,
                f"Profile was not updated: {error}"
            )