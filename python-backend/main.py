from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import pymongo
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
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
    expose_headers=["*"],
)

uri = os.getenv("MONGO_DB_URI")
client = pymongo.MongoClient(
    uri,
    tls=True,
    tlsAllowInvalidCertificates=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000
)

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    raise

db = client["ecommerce"]
collection = db["products"]

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
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": request.prompt}
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": request.prompt}
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            stream=False,
            stop=request.stop_sequences
        )       
        message_content = response.choices[0].message.content
        print(message_content)
        return message_content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
if __name__ == "__main__":  
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)