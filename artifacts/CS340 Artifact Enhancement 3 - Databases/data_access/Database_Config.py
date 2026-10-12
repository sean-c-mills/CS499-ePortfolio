# Imports operating-system tools used to read environment variables
import os

# Loads the MongoDB connection settings from environment variables
def get_database_config():

    # Reads the MongoDB username without storing it in the source code
    username = os.getenv(
        "AAC_MONGO_USERNAME"
    )

    # Reads the MongoDB password without storing it in the source code
    password = os.getenv(
        "AAC_MONGO_PASSWORD"
    )

    # Stops the application when required credentials aren't available
    if not username or not password:
        raise RuntimeError(
            "MongoDB credentials are missing. "
            "Set AAC_MONGO_USERNAME and AAC_MONGO_PASSWORD "
            "before starting the application."
        )

    # Returns the connection settings used by the data-access layer
    return {
        "username": username,
        "password": password,
        "host": os.getenv(
            "AAC_MONGO_HOST",
            "localhost"
        ),
        "port": int(
            os.getenv(
                "AAC_MONGO_PORT",
                "27017"
            )
        ),
        "database": os.getenv(
            "AAC_MONGO_DATABASE",
            "aac"
        )
    }