from fastapi import APIRouter, HTTPException, Request
from app.models.chat import ChatMessage, ChatResponse
from app.services.chat_service import ChatService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize chat service
try:
    chat_service = ChatService()
except Exception as e:
    logger.error(f"Failed to initialize chat service: {str(e)}")
    chat_service = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatMessage):
    """
    Handle chat messages with e-commerce context.
    """
    if chat_service is None:
        raise HTTPException(
            status_code=503,
            detail="Chat service is not available. Please try again later."
        )

    try:
        logger.info(f"Received chat request: {request.message[:100]}...")
        response = await chat_service.process_chat(request)
        logger.info(f"Generated response: {response.response[:100]}...")
        return response
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in chat endpoint: {error_msg}", exc_info=True)
        
        if "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again in a moment."
            )
        elif "api key" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Service configuration error. Please try again later."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred. Please try again."
            )
