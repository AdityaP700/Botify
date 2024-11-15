from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import pymongo
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="GROQ API with MongoDB and Pinecone")
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "chrome-extension://opjpegeohipcgfflbplaemjojfmmehon"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize MongoDB client
uri = os.getenv("MONGO_DB_URI")
client = pymongo.MongoClient(
    uri,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000,
    maxPoolSize=50
)

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    raise HTTPException(status_code=500, detail="Database connection error")

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: list[str] = ["Human:", "Assistant:"]

@app.post("/groq")
async def generate_groq_response(request: PromptRequest):
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.2-11b-text-preview",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant specialized in e-commerce. You provide accurate, relevant, and concise information about products and shopping."},
                {"role": "user", "content": request.prompt}
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            stream=False,
            stop=request.stop_sequences
        )
        
        # Extract the message content and return a properly formatted response
        message_content = response.choices[0].message.content
        return {
            "response": message_content,
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Error generating response from AI model",
                "message": str(e)
            }
        )

@app.get("/health")
async def health_check():
    try:
        # Check database connection
        client.admin.command('ping')
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)