import os
from dotenv import load_dotenv
from pathlib import Path

def load_environment():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    
    required_vars = [
        'PINECONE_API_KEY',
        'OPENAI_API_KEY',
        'GROQ_API_KEY',
        'MONGO_DB_URI'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

if __name__ == "__main__":
    load_environment()
    print("Environment variables loaded successfully!")
    print(f"PINECONE_API_KEY: {'*' * 10}{os.getenv('PINECONE_API_KEY')[-5:]}")
    print(f"OPENAI_API_KEY: {'*' * 10}{os.getenv('OPENAI_API_KEY')[-5:]}")
    print(f"GROQ_API_KEY: {'*' * 10}{os.getenv('GROQ_API_KEY')[-5:]}")
    print(f"MONGO_DB_URI: {'*' * 10}{os.getenv('MONGO_DB_URI')[-5:]}")
