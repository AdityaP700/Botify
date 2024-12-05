from app.models.conversation import Conversation
from app.database.mongo import mongodb
from app.core.logger import logger

class ConversationService:
    """Service for managing conversations in MongoDB."""
    
    @staticmethod
    async def store_conversation(user_message: str, bot_response: str, context: dict = None) -> bool:
        """
        Store a conversation in MongoDB.
        
        Args:
            user_message: The user's message
            bot_response: The bot's response
            context: Optional context information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conversation = Conversation(
                user_message=user_message,
                bot_response=bot_response,
                context=context
            )
            
            collection = mongodb.get_collection('conversations')
            await collection.insert_one(conversation.model_dump())
            
            logger.info(f"Stored conversation: {user_message[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error storing conversation: {str(e)}")
            return False
    
    @staticmethod
    async def get_recent_conversations(limit: int = 10):
        """
        Get recent conversations from MongoDB.
        
        Args:
            limit: Maximum number of conversations to retrieve
            
        Returns:
            list: List of recent conversations
        """
        try:
            collection = mongodb.get_collection('conversations')
            cursor = collection.find().sort('timestamp', -1).limit(limit)
            conversations = await cursor.to_list(length=limit)
            return conversations
            
        except Exception as e:
            logger.error(f"Error retrieving conversations: {str(e)}")
            return []
    
    @staticmethod
    async def get_user_context(user_id: str):
        """
        Get user's conversation context.
        
        Args:
            user_id: The user's identifier
            
        Returns:
            dict: User's context information
        """
        try:
            collection = mongodb.get_collection('user_context')
            context = await collection.find_one({'user_id': user_id})
            return context
            
        except Exception as e:
            logger.error(f"Error retrieving user context: {str(e)}")
            return None

conversation_service = ConversationService()
