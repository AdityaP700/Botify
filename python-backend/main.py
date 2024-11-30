from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from groq import Groq
from typing import Optional, Dict, Any, List
import os
import logging
import json
from datetime import datetime
from openai import OpenAI
from database.pinecone_client import index

# Initialize logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Config:
    """Application configuration."""
    ALLOWED_ORIGINS = ["chrome-extension://*", "http://localhost:3000"]
    MODEL_NAME = "text-embedding-3-small"
    DEFAULT_TOP_K = 3

class ChatMessage(BaseModel):
    """Schema for chat messages."""
    message: str = Field(..., description="The user's message")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the chat")

class ChatResponse(BaseModel):
    """Schema for chat responses."""
    response: str = Field(..., description="The AI's response")
    status: str = Field("success", description="Response status")

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str = Field(..., description="Error details")
    status: str = Field("error", description="Error status")

# Initialize FastAPI app
app = FastAPI(
    title="Botify API",
    description="AI-powered chat API with context-aware responses",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
try:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    groq_client = Groq(api_key=groq_api_key)
    logger.info("Successfully initialized API clients")
except Exception as e:
    logger.error(f"Client initialization error: {e}")
    raise RuntimeError(f"Failed to initialize API clients: {str(e)}")

async def get_relevant_context(query: str, k: int = Config.DEFAULT_TOP_K) -> str:
    """
    Get relevant context from Pinecone based on the query.
    
    Args:
        query: The user's query string
        k: Number of similar contexts to retrieve
        
    Returns:
        str: Combined relevant contexts
    """
    try:
        response = openai_client.embeddings.create(
            model=Config.MODEL_NAME,
            input=query
        )
        query_embedding = response.data[0].embedding
        
        search_response = index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True
        )
        
        contexts = [match.metadata.get('text', '') for match in search_response.matches]
        return "\n".join(contexts)
    except Exception as e:
        logger.error(f"Error getting relevant context: {e}")
        return ""

def format_context(context: Optional[Dict[str, Any]]) -> str:
    """
    Format the context data into a string for the AI model.
    
    Args:
        context: Dictionary containing context information
        
    Returns:
        str: Formatted context string
    """
    if not context:
        return ""
    
    formatted = []
    fields = {
        'title': 'Page Title',
        'description': 'Description',
        'url': 'Current URL'
    }
    
    for key, label in fields.items():
        if key in context:
            formatted.append(f"{label}: {context[key]}")
    
    return "\n".join(formatted)

@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        status.HTTP_200_OK: {"model": ChatResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}
    }
)
async def chat_endpoint(request: ChatMessage):
    try:
        # Get relevant context from Pinecone
        relevant_context = await get_relevant_context(request.message)
        
        # Format the context information from the request
        request_context = format_context(request.context) if request.context else ""
        
        # Combine both contexts
        full_context = f"{relevant_context}\n{request_context}".strip()
        
        # Prepare system message with e-commerce focus
        system_message = """You are a helpful AI shopping assistant. Your role is to:
        1. Help users find products they're looking for
        2. Compare prices and features
        3. Make product recommendations
        4. Answer questions about products
        5. Provide shopping advice
        
        Always be concise, accurate, and helpful. If you're unsure about something, say so."""
        
        if full_context:
            system_message += f"\n\nRelevant Context:\n{full_context}"
        
        # Generate response from Groq
        response = groq_client.chat.completions.create(
            model="llama-3.2-11b-text-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9,
            stream=False
        )

        # Extract response content
        response_content = response.choices[0].message.content
        
        # Log the interaction
        logger.info(f"Chat interaction - User: {request.message[:100]}... Response: {response_content[:100]}...")
        
        return ChatResponse(response=response_content)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint to verify API status."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)