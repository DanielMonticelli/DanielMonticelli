from os import path


class Config:
    input_file = path.join(
        path.dirname(path.dirname(__file__)), "data\\input\\data.csv"
    )
    mongo_uri = "mongodb://localhost:27017/"
    db_name = "etl_db"
    collection_name = "people"
