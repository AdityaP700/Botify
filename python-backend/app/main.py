from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Botify API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Botify API is running"}

@app.get("/test")
async def test():
    """Test endpoint that doesn't use any AI services"""
    return {
        "status": "success",
        "message": "Test endpoint is working",
        "service": "Botify API"
    }
