from db.mongo_connection import MongoConnection
from typing import List, Dict


class Loader:

    def __init__(self, mongo_connection: MongoConnection):
        """Recive mongodb connection

        Args:
            mongo_connection (MongoConnection): Connection to mongodb
        """

        self.mongo_connection = mongo_connection

    def load_to_mongo(self, data: List[Dict]):
        """Load data to mongodb

        Args:
            data (List[Dict]): Data from CSV file
        """

        self.mongo_connection.collection.insert_many(data)
