from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Conversation(BaseModel):
    """Conversation model for storing chat history."""
    user_message: str
    bot_response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    context: Optional[dict] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
