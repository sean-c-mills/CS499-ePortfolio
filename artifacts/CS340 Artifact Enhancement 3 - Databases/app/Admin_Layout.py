# Import Dash components that are used to build the page layout
from dash import dcc, html

# Import the function used to retrieve rescue-profile options
from services.Rescue_Profile_Service import get_profile_options

# Create the rescue-profile configuration page
def create_admin_layout(shelter):

    # Load the rescue profiles currently stored in MongoDB
    profile_options = get_profile_options(shelter)

    # Add an option that allows a new rescue profile to be created
    profile_options.append(
        {
            "label": "Create New Rescue Profile",
            "value": "new"
        }
    )

    # Use the first rescue profile as the default when one exists
    default_profile = (
        profile_options[0]["value"]
        if len(profile_options) > 1
        else "new"
    )
    
    return html.Div([

        # Displays the page title
        html.H1(
            "Rescue Profile Configuration"
        ),

        # Creates a button that will return the user to the main dashboard
        dcc.Link(
            html.Button(
                "Return to Dashboard"
            ),
            href="/"
        ),

        # Separate the page header from the configuration controls
        html.Hr(),

        # Used to label the rescue-profile dropdown
        html.Label(
            "Rescue Profile:"
        ),

        # Allows the user to select which rescue profile to edit
        dcc.Dropdown(
            id="profile-manager-type",

            # Uses the rescue profiles stored in MongoDB
            options=profile_options,

            # Uses the first rescue profile as the selected default
            value=default_profile,
            clearable=False,

            style={
                "width": "500px",
                "marginBottom": "15px"
            }
        ),

        # Label for the rescue-profile name
        html.Label(
            "Profile Name:"
        ),

        # Allows the rescue-profile name to be entered
        dcc.Input(
            id="profile-name",
            type="text",

            style={
                "display": "block",
                "width": "500px",
                "marginBottom": "15px"
            }
        ),

        # Label for the preferred breeds field
        html.Label(
            "Preferred Breeds:"
        ),

        # Explains to the user how multiple breeds should be entered
        html.P(
            "Enter multiple breeds separated by commas."
        ),

        # Allows the preferred breeds to be entered as text
        dcc.Textarea(
            id="profile-breeds",

            style={
                "width": "500px",
                "height": "100px",
                "marginBottom": "15px"
            }
        ),

        # Add spacing before the next field
        html.Br(),

        # Label the sex-requirement dropdown
        html.Label(
            "Sex Requirement:"
        ),

        # Allow the required sex to be selected
        dcc.Dropdown(
            id="profile-sex",

            # Define the available sex values
            options=[
                {
                    "label": "Intact Female",
                    "value": "Intact Female"
                },
                {
                    "label": "Intact Male",
                    "value": "Intact Male"
                },
                {
                    "label": "Spayed Female",
                    "value": "Spayed Female"
                },
                {
                    "label": "Neutered Male",
                    "value": "Neutered Male"
                }
            ],

            clearable=False,

            style={
                "width": "500px",
                "marginBottom": "15px"
            }
        ),

        # Label the minimum age field
        html.Label(
            "Minimum Age in Weeks:"
        ),

        # Allows the minimum rescue age to be entered
        dcc.Input(
            id="profile-min-age",
            type="number",
            min=0,
            step=1,

            style={
                "display": "block",
                "width": "200px",
                "marginBottom": "15px"
            }
        ),

        # Label the maximum age field
        html.Label(
            "Maximum Age in Weeks:"
        ),

        # Allow the maximum rescue age to be entered
        dcc.Input(
            id="profile-max-age",
            type="number",
            min=0,
            step=1,

            style={
                "display": "block",
                "width": "200px",
                "marginBottom": "15px"
            }
        ),

        # Groups the profile action buttons together
        html.Div(
            [

                # Creates the button that is used to save the profile changes
                html.Button(
                    "Save Profile",
                    id="save-profile-button",
                    n_clicks=0
                ),

                # Creates a confirmation prompt before deleting a rescue profile
                dcc.ConfirmDialogProvider(
                    id="delete-profile-confirm",
                    message=(
                        "Are you sure you want to delete this rescue profile?"
                    ),

                    children=html.Button(
                        "Delete Profile"
                    )
                )
            ],

            # Displays the buttons beside each other with spacing
            style={
                "display": "flex",
                "gap": "10px"
            }
        ),

        # Displays a success or validation message after saving or deleting
        html.Div(
            id="profile-save-status",

            style={
                "marginTop": "15px",
                "fontWeight": "bold"
            }
        )
    ])