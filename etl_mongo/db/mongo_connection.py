from pymongo import MongoClient


class MongoConnection:

    def __init__(self, uri: str, db_name: str, collection_name: str):
        """Set Mongodb connection configurations

        Args:
            uri (str): URI to mongodb
            db_name (str): Mongodb database name
            collection_name (str): Database collection name
        """

        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """Open connection to mongodb"""

        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def close(self):
        """Close connection to mongodb"""

        if self.client:
            self.client.close()
