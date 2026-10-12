# Imports the Dash callback tools
from dash import Input, Output, State, no_update, ctx

# Imports the functions used to validate rescue profiles
from services.Rescue_Profiles import (
    create_profile_type,
    validate_profile
)

# Imports the functions used to work with rescue profiles in MongoDB
from services.Rescue_Profile_Service import (
    delete_profile,
    get_profile,
    get_profile_options,
    save_profile
)

# Registers the callbacks used by the rescue-profile configuration page
def register_admin_callbacks(app, shelter):

    # Loads the selected rescue profile when the profile type changes
    @app.callback(
        [
            Output(
                "profile-name",
                "value"
            ),

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

        Input(
            "profile-manager-type",
            "value"
        )
    )
    def load_profile_editor(profile_type):

        # Clears the fields when a new rescue profile is being created
        if profile_type == "new":
            return (
                "",
                "",
                None,
                None,
                None
            )

        # Gets the selected rescue profile from MongoDB
        profile = get_profile(
            shelter,
            profile_type
        )

        # Converts the breed list into text for the breed field
        breeds_text = ", ".join(
            profile["breeds"]
        )

        # Returns the profile values to the configuration fields
        return (
            profile["label"],
            breeds_text,
            profile["sex"],
            profile["min_age_weeks"],
            profile["max_age_weeks"]
        )

    # Saves or deletes a rescue profile when the corresponding button is selected
    @app.callback(
        [
            Output(
                "profile-manager-type",
                "options"
            ),

            Output(
                "profile-manager-type",
                "value"
            ),

            Output(
                "profile-save-status",
                "children"
            )
        ],

        [
            Input(
                "save-profile-button",
                "n_clicks"
            ),

            Input(
                "delete-profile-confirm",
                "submit_n_clicks"
            )
        ],

        [
            State(
                "profile-manager-type",
                "value"
            ),

            State(
                "profile-name",
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

        # Doesn't run the callback when the page first loads
        prevent_initial_call=True
    )
    def manage_rescue_profile(
        save_clicks,
        delete_clicks,
        selected_profile_type,
        profile_name,
        breeds_text,
        sex,
        min_age_weeks,
        max_age_weeks
    ):

        # Deletes the selected profile when the delete button is used
        if ctx.triggered_id == "delete-profile-confirm":

            # Prevents the New Profile option from being deleted
            if selected_profile_type == "new":
                return (
                    no_update,
                    no_update,
                    "Select an existing profile to delete."
                )

            # Gets the profile name before deleting the record
            profile = get_profile(
                shelter,
                selected_profile_type
            )

            profile_label = profile[
                "label"
            ]

            # Deletes the selected profile from MongoDB
            deleted_count = delete_profile(
                shelter,
                selected_profile_type
            )

            # Displays an error if no profile was deleted
            if deleted_count == 0:
                return (
                    no_update,
                    no_update,
                    "The rescue profile could not be deleted."
                )

            # Reloads the remaining rescue profiles from MongoDB
            profile_options = get_profile_options(
                shelter
            )

            # Selects the first remaining profile when one is available
            default_profile = (
                profile_options[0]["value"]
                if profile_options
                else "new"
            )

            # Adds the option used to create a new rescue profile
            profile_options.append(
                {
                    "label": "Create New Rescue Profile",
                    "value": "new"
                }
            )

            # Displays the remaining profiles and confirms the deletion
            return (
                profile_options,
                default_profile,
                f"{profile_label} was deleted successfully."
            )

        # Starts with an empty breed list
        breeds = []

        # Splits the breed text into individual values
        if breeds_text:
            breeds = [
                breed.strip()
                for breed in breeds_text.split(",")
                if breed.strip()
            ]

        try:
            # Creates a new profile identifier when a new profile is being added
            if selected_profile_type == "new":
                profile_type = create_profile_type(
                    profile_name
                )

            # Keeps the existing identifier when a profile is being updated
            else:
                profile_type = selected_profile_type

            # Validates the profile values before saving them
            profile = validate_profile(
                profile_type,
                profile_name,
                breeds,
                sex,
                min_age_weeks,
                max_age_weeks
            )

            # Saves the validated profile to MongoDB
            save_profile(
                shelter,
                profile
            )

            # Reloads the rescue-profile options from MongoDB
            profile_options = get_profile_options(
                shelter
            )

            # Adds the option used to create another rescue profile
            profile_options.append(
                {
                    "label": "Create New Rescue Profile",
                    "value": "new"
                }
            )

            # Shows the saved profile and a success message
            return (
                profile_options,
                profile_type,
                f"{profile['label']} was saved successfully."
            )

        except ValueError as error:
            # Keeps the current values when validation fails
            return (
                no_update,
                no_update,
                f"Profile was not saved: {error}"
            )