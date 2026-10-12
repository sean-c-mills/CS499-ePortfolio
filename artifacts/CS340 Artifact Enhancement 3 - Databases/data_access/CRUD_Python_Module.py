# Imports the MongoDB client used to connect to the database
from pymongo import MongoClient

# CRUD operations for the Animal collection in MongoDB
class AnimalShelter(object):
    
    def __init__(
        self,
        username,
        password,
        host="localhost",
        port=27017,
        database_name="aac"
    ):
        # Initializing the MongoClient. This provides access to the MongoDB
        # database and animal collection used by the application

        # Connection variables
        HOST = host
        PORT = port
        DB = database_name
        COL = "animals"

        # Initialize connection
        self.client = MongoClient(
            "mongodb://%s:%s@%s:%d"
            % (
                username,
                password,
                HOST,
                PORT
            )
        )

        self.database = self.client[DB]
        self.collection = self.database[COL]

    # Returns another collection from the same MongoDB database
    def get_collection(self, collection_name):
        # Allows other services to work with collections besides animals
        return self.database[collection_name]

    # Implements the C (create) operation in CRUD
    def create(self, data):
        # Makes sure data is provided before attempting an insert
        if data is not None:
            try:
                # Attempts to insert the document into the collection
                self.collection.insert_one(data)

                # Returns True if the insert is successful
                return True

            except Exception as e:
                # Catches and displays errors that happen during insertion
                print(f"Insert failed: {e}")

                # Returns False to show there was an error
                return False

        else:
            # Returns False if no data was provided
            return False

    # Implements the R (read) operation in CRUD
    def read(self, query):
        try:
            # Executes a MongoDB find query using the supplied criteria
            results = self.collection.find(query)

            # Converts the MongoDB cursor to a list and returns the records
            return list(results)

        except Exception as e:
            # Catches and displays errors that happen during the query
            print(f"Read failed: {e}")

            # Returns an empty list if the query fails
            return []

    # Implements the U (update) operation in CRUD
    def update(self, query, new_values):
        try:
            # Updates all documents that match the supplied query
            result = self.collection.update_many(
                query,
                {
                    "$set": new_values
                }
            )

            # Returns the number of documents that were modified
            return result.modified_count

        except Exception as e:
            # Catches and displays errors that happen during the update
            print(f"Update failed: {e}")

            # Returns zero if the update fails
            return 0

    # Implements the D (delete) operation in CRUD
    def delete(self, query):
        try:
            # Deletes all documents that match the supplied query
            result = self.collection.delete_many(query)

            # Returns the number of documents that were deleted
            return result.deleted_count

        except Exception as e:
            # Catches and displays errors that happen during deletion
            print(f"Delete failed: {e}")

            # Returns zero if the deletion fails
            return 0

    # Closes the MongoDB connection when it is no longer needed
    def close(self):
        self.client.close()