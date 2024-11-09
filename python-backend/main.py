from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import pymongo
import pinecone
import os
from dotenv import load_dotenv
import datetime
import random

load_dotenv()

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))
index_name = "your_index_name"  # Ensure this matches your Pinecone setup
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=384)  # Adjust dimension per embedding model
index = pinecone.Index(index_name)

uri = os.getenv("MONGO_DB_URI")
client = pymongo.MongoClient(
    uri,
    tls=True,
    tlsAllowInvalidCertificates=True,  # Use in development only, not recommended for production
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

app = FastAPI(title="GROQ API with MongoDB and Pinecone")

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
                {"role": "system", "content": "hi groq"},
                {"role": "user", "content": request.prompt},
                {"role": "assistant", "content": ""}
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            stream=False,
            stop=request.stop_sequences
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PineconeRequest(BaseModel):
    id: str
    description: str

@app.post("/pinecone/upsert")
async def upsert_to_pinecone(request: PineconeRequest):
    try:
        embedding = [random.random() for _ in range(384)]  # Placeholder for embedding vector
        
        index.upsert([(request.id, embedding, {"description": request.description})])
        return {"status": "success", "message": "Data upserted to Pinecone"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
