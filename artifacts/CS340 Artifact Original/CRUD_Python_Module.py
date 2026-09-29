# Python Code to Insert a Document 
# Sean Mills - CS340 - SNHU

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # Connection Variables 
        # 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient(
            'mongodb://%s:%s@%s:%d' % (username, password, HOST, PORT)
        ) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
             
    # Create method to implement the C (create) in CRUD
    def create(self, data):
        # Makes sure data is provided before attempting insert
        if data is not None: 
            try:
                # Attempts to insert the document into the collection
                self.collection.insert_one(data)

                # Return True if the insert is successful
                return True        

            except Exception as e:
                # Will catch and then display any errors that happens during insertion
                print(f"Insert failed: {e}")

                # Returns False to show there was an error
                return False
        else:
            # Return False if no data was provided
            return False

    # Create method to implement the R (read) in CRUD.
    def read(self, query):
        try: 
            # Executes a MongoDB find query by using the key/value pair
            results = self.collection.find(query)
            
            # Converts cursor results to a list and returns
            return list(results)

        except Exception as e:
            # Catches and displays any errors that happen during the query
            print(f"Read failed: {e}")

            # Return an empty list if the query fails
            return []
    
    # Create method to implement the U (update) in CRUD
    def update(self, query, new_values):
        try:
            # Updates the documents that match the query
            result = self.collection.update_many(
                query, {"$set": new_values}
            )

            # Returns the number of documents that are modified
            return result.modified_count

        except Exception as e:
            # Catches and displays any errors that happen during the update
            print(f"Update failed: {e}")

            # Returns zero if the update were to fail
            return 0

    # Create method to implement the D (delete) in CRUD
    def delete(self, query):
        try:
            # Deletes the documents that match the query
            result = self.collection.delete_many(query)

            # Returns the number of documents that are deleted
            return result.deleted_count
      
        except Exception as e:
            # Catches and displays any errors that happen during deletion
            print(f"Delete failed: {e}")

            # Returns zero if the deletion fails
            return 0