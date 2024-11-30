import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = "botify"
MONGO_COLLECTION_NAME = "conversations"
