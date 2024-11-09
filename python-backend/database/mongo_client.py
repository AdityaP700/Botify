from pymongo import MongoClient
from config.mongo_config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

def get_data_from_mongo():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    data = list(collection.find({}, {"_id": 1, "description": 1}))
    return data
