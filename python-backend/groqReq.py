import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Initialize the GROQ client
client = Groq(
    api_key="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"
)

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: list[str] = ["Human:", "Assistant:"]

@app.post("/groq")
async def generate_groq_response(request: PromptRequest):
    try:
        chat_completion = client.chat.completions.create(
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

        return {"res":chat_completion.choices[0].message}

        
    except Exception as e:
        print(f"Error calling GROQ: {e}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)