# Imports Dash components used by the dashboard callbacks
from dash import Input, Output, dcc, html

# Imports libraries used for the map, data processing, and chart
import dash_leaflet as dl
import pandas as pd
import plotly.express as px

# Imports the function used to retrieve animals by type
from services.Animal_Service import get_animals_by_type

# Imports the functions used to work with rescue profiles
from services.Rescue_Profiles import (
    get_default_profiles,
    get_profile
)

# Imports the function used to retrieve rescue candidates
from services.Rescue_Service import get_rescue_animals

# Map display settings
MAP_ZOOM = 10
MAP_WIDTH = "1000px"
MAP_HEIGHT = "500px"

# Registers the callbacks used by the main dashboard
def register_callbacks(app, shelter):

    # Updates the animal table when the dashboard selections change
    @app.callback(
        [
            Output(
                "datatable-id",
                "data"
            ),

            Output(
                "datatable-id",
                "selected_rows"
            )
        ],

        [
            Input(
                "main-tabs",
                "value"
            ),

            Input(
                "browse-animal-type",
                "value"
            ),

            Input(
                "filter-type",
                "value"
            ),

            Input(
                "rescue-profile-store",
                "data"
            )
        ]
    )
    def update_dashboard(
        active_tab,
        animal_type,
        filter_type,
        profiles
    ):

        # Retrieves animals by type whenever the Browse Animals tab is selected
        if active_tab == "browse":

            display_dataframe = get_animals_by_type(
                shelter,
                animal_type
            )

        # Retrieves animals that match the selected rescue profile
        else:

            # Loads the default profiles if the session data isn't available
            if profiles is None:
                profiles = get_default_profiles()

            # Retrieves the selected rescue profile
            profile = get_profile(
                profiles,
                filter_type
            )

            # Retrieves animals that meet the rescue requirements
            display_dataframe = get_rescue_animals(
                shelter,
                profile
            )

        # Selects the first animal whenever results are available
        selected_rows = (
            [0]
            if not display_dataframe.empty
            else []
        )

        # Returns the animal records and selected rows to the table
        return (
            display_dataframe.to_dict(
                "records"
            ),
            selected_rows
        )

    # Updates the breed chart using the animals currently shown in the table
    @app.callback(
        Output(
            "graph-id",
            "children"
        ),

        Input(
            "datatable-id",
            "derived_virtual_data"
        )
    )
    def update_graphs(view_data):

        # Stops if the table data isn't available
        if view_data is None:
            return

        # Converts the visible table records into a DataFrame
        display_dataframe = pd.DataFrame(
            view_data
        )

        # Displays a message when no animals match the current selection
        if display_dataframe.empty:
            return html.H4(
                "No animals match the current selection."
            )

        # Displays a message if the breed information isn't available
        if "breed" not in display_dataframe.columns:
            return html.H4(
                "Breed information is unavailable."
            )

        # Counts how many animals belong to each breed
        breed_count = (
            display_dataframe["breed"]
            .value_counts()
            .reset_index()
        )

        # Names the columns used by the chart
        breed_count.columns = [
            "breed",
            "count"
        ]

        # Limits the chart to the ten most common breeds
        top_breeds = breed_count.head(
            10
        )

        # Creates the breed distribution pie chart
        figure = px.pie(
            top_breeds,
            names="breed",
            values="count",
            title="Top 10 Breed Distribution"
        )

        # Adjusts the position of the chart title
        figure.update_layout(
            title_x=0.27
        )

        # Displays the completed chart
        return [
            dcc.Graph(
                figure=figure
            )
        ]

    # Highlights columns that are selected by the user
    @app.callback(
        Output(
            "datatable-id",
            "style_data_conditional"
        ),

        Input(
            "datatable-id",
            "selected_columns"
        )
    )
    def update_styles(selected_columns):

        # Returns the default table style if no columns are selected
        if selected_columns is None:
            return []

        # Applies a background color to each selected column
        return [
            {
                "if": {
                    "column_id": column
                },
                "background_color": "#D2F3FF"
            }
            for column in selected_columns
        ]

    # Updates the map whenever an animal is selected from the table
    @app.callback(
        Output(
            "map-id",
            "children"
        ),

        [
            Input(
                "datatable-id",
                "derived_virtual_data"
            ),

            Input(
                "datatable-id",
                "derived_virtual_selected_rows"
            )
        ]
    )
    def update_map(
        view_data,
        selected_rows
    ):

        # Stops if the table data isn't available
        if view_data is None:
            return

        # Converts the visible table records into a DataFrame
        display_dataframe = (
            pd.DataFrame.from_dict(
                view_data
            )
        )

        # Stops if the table doesn't contain any animal records
        if display_dataframe.empty:
            return

        # Uses the first animal if no row is selected
        if not selected_rows:
            row = 0
        else:
            row = selected_rows[0]

        # Resets the selection if the stored row isn't valid anymore
        if (
            row < 0
            or row >= len(display_dataframe)
        ):
            row = 0

        # Retrieves the animal selected from the table
        selected_animal = (
            display_dataframe.iloc[row]
        )

        # Checks that the selected animal contains location fields
        if (
            "location_lat"
            not in selected_animal.index
            or "location_long"
            not in selected_animal.index
        ):
            return html.H4(
                "Location information is unavailable."
            )

        # Retrieves the animal's latitude and longitude
        latitude = selected_animal[
            "location_lat"
        ]

        longitude = selected_animal[
            "location_long"
        ]

        # Displays a message if the location values are missing
        if (
            pd.isna(latitude)
            or pd.isna(longitude)
        ):
            return html.H4(
                "Location information is unavailable."
            )

        # Retrieves the animal name for the map popup
        animal_name = selected_animal.get(
            "name",
            "N/A"
        )

        # Replaces a missing animal name with a default value
        if (
            pd.isna(animal_name)
            or str(animal_name).strip() == ""
        ):
            animal_name = "N/A"

        # Retrieves the animal breed for the map tooltip
        animal_breed = selected_animal.get(
            "breed",
            "Breed unavailable"
        )

        # Replaces a missing breed with a default value
        if (
            pd.isna(animal_breed)
            or str(animal_breed).strip() == ""
        ):
            animal_breed = "Breed unavailable"

        # Creates the map that is centered on the selected animal
        return [
            dl.Map(
                style={
                    "width": MAP_WIDTH,
                    "height": MAP_HEIGHT
                },

                center=[
                    latitude,
                    longitude
                ],

                zoom=MAP_ZOOM,

                children=[

                    # Displays the base map layer
                    dl.TileLayer(
                        id="base-layer-id"
                    ),

                    # Places a marker at the animal's location
                    dl.Marker(
                        position=[
                            latitude,
                            longitude
                        ],

                        children=[

                            # Displays the breed whenever the marker is hovered over
                            dl.Tooltip(
                                str(
                                    animal_breed
                                )
                            ),

                            # Displays the animal name whenever the marker is selected
                            dl.Popup([

                                html.H1(
                                    "Animal Name"
                                ),

                                html.P(
                                    str(
                                        animal_name
                                    )
                                )
                            ])
                        ]
                    )
                ]
            )
        ]