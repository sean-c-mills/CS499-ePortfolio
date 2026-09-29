# Import Dash components that are used to build the page layout
from dash import dcc, html

# Create the rescue-profile configuration page
def create_admin_layout():
    
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

            # Defines the available rescue profiles
            options=[
                {
                    "label": "Water Rescue",
                    "value": "water"
                },
                {
                    "label": "Mountain or Wilderness Rescue",
                    "value": "mountain"
                },
                {
                    "label": "Disaster or Individual Tracking",
                    "value": "disaster"
                }
            ],

            # Use Water Rescue as the selected default
            value="water",
            clearable=False,

            style={
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

        # Creates the button that is used to save the profile changes
        html.Button(
            "Save Profile",
            id="save-profile-button",
            n_clicks=0
        ),

        # Displays a success or validation message after saving
        html.Div(
            id="profile-save-status",

            style={
                "marginTop": "15px",
                "fontWeight": "bold"
            }
        )
    ])