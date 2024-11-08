from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import pymongo
import os
from dotenv import load_dotenv
import datetime  # Import datetime
import random

load_dotenv()

# MongoDB connection with SSL settings
uri = os.getenv("MONGO_DB_URI")

client = pymongo.MongoClient(
    uri,
    tls=True,                     # Correct SSL/TLS option
    tlsAllowInvalidCertificates=True,  # Use in development only, not recommended for production
    serverSelectionTimeoutMS=5000
)

try:
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    raise

db = client["ecommerce"]
collection = db["products"]

# GROQ client
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Create FastAPI app instance
app = FastAPI(title="GROQ API with MongoDB")

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: list[str] = ["Human:", "Assistant:"]

@app.post("/groq")
async def generate_groq_response(request: PromptRequest):
    try:
        # Generate response using GROQ
        response = groq_client.chat.completions.create(
            model="llama-3.2-11b-text-preview",
            messages=[
                {
                    "role": "system",
                    "content": "hi groq"
                },
                {
                    "role": "user",
                    "content": request.prompt
                },
                {
                    "role": "assistant",
                    "content": ""
                }
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            stream=False,
            stop=request.stop_sequences
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
