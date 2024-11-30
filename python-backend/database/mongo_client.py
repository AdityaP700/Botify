from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging
from bson import ObjectId
import sys
from pathlib import Path

# Add the parent directory to the Python path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Get MongoDB client instance"""
    mongo_uri = os.getenv("MONGO_DB_URI")
    if not mongo_uri:
        raise ValueError("MONGO_DB_URI environment variable not set")
    return MongoClient(mongo_uri)

def get_data_from_mongo():
    """Get data from MongoDB collection"""
    try:
        client = get_mongo_client()
        db = client["botify"]
        collection = db["conversations"]
        data = list(collection.find({}, {"_id": 1, "description": 1}))
        logger.info(f"Retrieved {len(data)} documents from MongoDB")
        return data
    except Exception as e:
        logger.error(f"Error retrieving data from MongoDB: {e}")
        return []

def insert_sample_data():
    """Insert sample data into MongoDB for testing"""
    try:
        client = get_mongo_client()
        db = client["botify"]
        collection = db["conversations"]
        
        # Sample data
        sample_data = [
            {
                "_id": ObjectId(),
                "description": "High-quality wireless headphones with noise cancellation feature. Perfect for music lovers and professionals.",
                "product_type": "Electronics",
                "price": 199.99
            },
            {
                "_id": ObjectId(),
                "description": "Premium leather wallet with RFID protection. Multiple card slots and sleek design.",
                "product_type": "Accessories",
                "price": 49.99
            },
            {
                "_id": ObjectId(),
                "description": "Smart fitness tracker with heart rate monitoring and sleep tracking. Water-resistant and long battery life.",
                "product_type": "Electronics",
                "price": 79.99
            }
        ]
        
        # Insert the sample data
        result = collection.insert_many(sample_data)
        logger.info(f"Inserted {len(result.inserted_ids)} sample documents into MongoDB")
        return result.inserted_ids
        
    except Exception as e:
        logger.error(f"Error inserting sample data into MongoDB: {e}")
        return None

if __name__ == "__main__":
    # Insert sample data
    logger.info("Inserting sample data into MongoDB...")
    insert_sample_data()
    
    # Verify the data
    logger.info("\nRetrieving data from MongoDB...")
    data = get_data_from_mongo()
    logger.info(f"Found {len(data)} documents in MongoDB")
