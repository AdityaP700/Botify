from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from load_env import load_environment

# Load environment variables
load_environment()

# Get MongoDB URI from environment variables
uri = os.getenv("MONGODB_URI")
if not uri:
    raise ValueError("MONGODB_URI environment variable is not set")

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"MongoDB connection error: {e}")