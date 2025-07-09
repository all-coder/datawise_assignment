from pymongo import MongoClient

def get_db(mongo_uri: str = "mongodb://localhost:27017/", db_name: str = "catalog"):
    client = MongoClient(mongo_uri)
    return client[db_name]

