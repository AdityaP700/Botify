from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection
uri = "mongodb+srv://divyanshushekhar987:dfLgt7Op3DalQW0A@cluster0.yr2fg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.your_database_name  # Replace with your actual database name

# GROQ client
groq_client = Groq(
    api_key="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"
)

app = FastAPI()

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

        # Save the generated text to MongoDB
        db.your_collection_name.insert_one({"prompt": request.prompt, "response": generated_text})

        return {"result": generated_text}
    except Exception as e:
        print(f"Error calling GROQ: {e}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)