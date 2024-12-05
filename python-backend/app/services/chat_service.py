from app.models.chat import ChatMessage, ChatResponse
from app.core.config import settings
from app.core.logger import logger
import openai
from typing import Optional, Dict, Any

class ChatService:
    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = None
        if not settings.OPENAI_API_KEY:
            raise Exception("OpenAI API key is required")
        
        try:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai.Client()
            self.model = "gpt-3.5-turbo"  # Using GPT-3.5 for better cost efficiency
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise

    def _prepare_system_message(self, context: Optional[Dict[str, Any]] = None) -> str:
        """Prepare the system message with context"""
        system_message = """You are a helpful AI shopping assistant. Help users with:
        1. Finding products
        2. Comparing prices and features
        3. Making recommendations
        4. Answering product questions
        Always be concise and helpful."""

        if context:
            url = context.get('url', '')
            title = context.get('title', '')
            if url and title:
                system_message += f"\nUser is currently viewing: {title} at {url}"

        return system_message

    async def process_chat(self, request: ChatMessage) -> ChatResponse:
        """Process chat messages using OpenAI"""
        try:
            messages = [
                {"role": "system", "content": self._prepare_system_message(request.context)},
                {"role": "user", "content": request.message}
            ]

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            
            return ChatResponse(response=response.choices[0].message.content)

        except Exception as e:
            logger.error(f"Error in chat service: {str(e)}")
            error_msg = "I apologize, but I'm having trouble processing your request."
            if "rate_limit" in str(e).lower():
                error_msg += " The service is currently experiencing high demand. Please try again in a moment."
            return ChatResponse(response=error_msg)
