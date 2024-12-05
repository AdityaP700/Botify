from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChatMessage(BaseModel):
    """
    Chat message model with optional context.
    """
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """
    Chat response model.
    """
    response: str
