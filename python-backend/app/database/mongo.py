from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.logger import logger

class MongoDB:
    client: AsyncIOMotorClient = None
    
    async def connect_to_database(self):
        """
        Create database connection.
        """
        try:
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                tls=True,
                tlsAllowInvalidCertificates=True,
                maxPoolSize=50
            )
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise
    
    async def close_database_connection(self):
        """
        Close database connection.
        """
        try:
            self.client.close()
            logger.info("Closed MongoDB connection")
        except Exception as e:
            logger.error(f"Could not close MongoDB connection: {e}")
            raise
    
    def get_collection(self, collection_name: str):
        """
        Get a collection from the database.
        """
        return self.client[settings.MONGODB_DB_NAME][collection_name]
    
    async def store_conversation(self, user_message: str, bot_response: str):
        """
        Store a conversation in MongoDB.
        """
        try:
            collection = self.get_collection(settings.MONGODB_COLLECTION)
            await collection.insert_one({
                "user_message": user_message,
                "bot_response": bot_response,
                "timestamp": datetime.utcnow()
            })
            logger.info("Stored conversation in MongoDB")
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
            # Don't raise the exception to avoid interrupting chat flow
            
mongodb = MongoDB()
