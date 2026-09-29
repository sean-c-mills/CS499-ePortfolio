# Imports tools used to locate and encode the dashboard logo
from pathlib import Path
import base64

# Imports Dash components used to build the dashboard layout
from dash import dcc, html, dash_table

# Sets the number of animal records shown on each table page
PAGE_SIZE = 10

# Loads and encodes the dashboard logo for display in Dash
def encode_logo():

    # Builds the path to the logo stored in the assets folder
    image_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "Grazioso Salvare Logo.png"
    )

    # Reads the image and converts it into a format Dash can display
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()

# Creates the main Animal Shelter Dashboard layout
def create_dashboard_layout(initial_dataframe):

    # Loads the encoded logo used in the dashboard header
    encoded_image = encode_logo()

    # Defines the animal types available in the browsing dropdown
    animal_type_options = [
        {
            "label": "All Animals",
            "value": "all"
        },
        {
            "label": "Bird",
            "value": "Bird"
        },
        {
            "label": "Cat",
            "value": "Cat"
        },
        {
            "label": "Dog",
            "value": "Dog"
        },
        {
            "label": "Rabbit",
            "value": "Rabbit"
        },
        {
            "label": "Other",
            "value": "Other"
        }
    ]

    # Builds the complete dashboard interface
    return html.Div([

        # Displays the dashboard title
        html.Center(
            html.B(
                html.H1(
                    "Animal Shelter Dashboard - Sean Mills"
                )
            )
        ),

        # Displays the Grazioso Salvare logo with a link to SNHU's website
        html.Center(
            html.A(
                html.Img(
                    src=(
                        "data:image/png;base64,"
                        + encoded_image
                    ),
                    style={
                        "height": "180px"
                    }
                ),
                href="https://www.snhu.edu",
                target="_blank"
            )
        ),

        # Creates a button that opens the rescue-profile configuration page
        html.Center(
            dcc.Link(
                html.Button(
                    "Rescue Profile Configuration"
                ),
                href="/admin"
            )
        ),

        # Separates the dashboard header from the main controls
        html.Hr(),

        # Creates tabs for general browsing and rescue-candidate searches
        dcc.Tabs(
            id="main-tabs",
            value="browse",

            children=[

                # Creates the tab used to browse shelter animals
                dcc.Tab(
                    label="Browse Animals",
                    value="browse",

                    children=[

                        # Groups the Browse Animals controls together
                        html.Div(
                            [

                                # Displays the Browse Animals section title
                                html.H2(
                                    "Browse Shelter Animals"
                                ),

                                # Explains the purpose of the browsing section
                                html.P(
                                    "Choose an animal type to view the shelter records."
                                ),

                                # Labels the animal-type dropdown
                                html.Label(
                                    "Animal Type:"
                                ),

                                # Allows the user to filter animals by type
                                dcc.Dropdown(
                                    id="browse-animal-type",
                                    options=animal_type_options,
                                    value="all",
                                    clearable=False,

                                    style={
                                        "width": "400px"
                                    }
                                )
                            ],

                            # Adds spacing around the browsing controls
                            style={
                                "padding": "20px"
                            }
                        )
                    ]
                ),

                # Creates the tab used to search for rescue candidates
                dcc.Tab(
                    label="Rescue Candidates",
                    value="rescue",

                    children=[

                        # Groups the Rescue Candidates controls together
                        html.Div(
                            [

                                # Displays the Rescue Candidates section title
                                html.H2(
                                    "Specialized Rescue Candidate Search"
                                ),

                                # Explains the purpose of the rescue search
                                html.P(
                                    "Find dogs that match the requirements for a selected rescue type."
                                ),

                                # Labels the rescue-type selection
                                html.Label(
                                    "Select Rescue Type:"
                                ),

                                # Allows the user to select a rescue profile
                                dcc.RadioItems(
                                    id="filter-type",

                                    # Defines the available rescue types
                                    options=[
                                        {
                                            "label": "Water Rescue",
                                            "value": "water"
                                        },
                                        {
                                            "label": (
                                                "Mountain or "
                                                "Wilderness Rescue"
                                            ),
                                            "value": "mountain"
                                        },
                                        {
                                            "label": (
                                                "Disaster or "
                                                "Individual Tracking"
                                            ),
                                            "value": "disaster"
                                        }
                                    ],

                                    # Uses Water Rescue as the selected default
                                    value="water",

                                    # Displays each rescue option on its own line
                                    labelStyle={
                                        "display": "block"
                                    }
                                )
                            ],

                            # Adds spacing around the rescue-search controls
                            style={
                                "padding": "20px"
                            }
                        )
                    ]
                )
            ]
        ),

        # Separates the search controls from the animal results
        html.Hr(),

        # Displays animal records returned by the current search
        dash_table.DataTable(
            id="datatable-id",

            # Creates table columns from the initial shelter data
            columns=[
                {
                    "name": column,
                    "id": column,
                    "deletable": False,
                    "selectable": True
                }
                for column
                in initial_dataframe.columns
            ],

            # Loads the initial animal records into the table
            data=initial_dataframe.to_dict(
                "records"
            ),

            # Allows one animal record to be selected at a time
            row_selectable="single",
            selected_rows=[0],

            # Limits the number of records displayed on each page
            page_size=PAGE_SIZE,

            # Allows the user to sort and filter the table
            sort_action="native",
            filter_action="native",

            # Allows horizontal scrolling when the table is wider than the page
            style_table={
                "overflowX": "auto"
            }
        ),

        # Adds spacing between the table and visual displays
        html.Br(),
        html.Hr(),

        # Places the breed chart and location map beside each other
        html.Div(
            className="row",

            style={
                "display": "flex"
            },

            children=[

                # Provides the location where the breed chart is displayed
                html.Div(
                    id="graph-id",
                    className="col s12 m6"
                ),

                # Provides the location where the animal map is displayed
                html.Div(
                    id="map-id",
                    className="col s12 m6"
                )
            ]
        )
    ])