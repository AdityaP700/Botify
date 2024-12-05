import os
from dotenv import load_dotenv
from pathlib import Path

def load_environment():
    """Load environment variables from .env file"""
    # Print current directory for debugging
    print(f"Current directory: {os.getcwd()}")
    
    # Get the directory containing this script
    current_dir = Path(__file__).parent
    env_file = current_dir / '.ENV'
    
    print(f"Looking for env file at: {env_file}")
    print(f"File exists: {env_file.exists()}")
    
    if not env_file.exists():
        raise ValueError(f"Environment file not found at {env_file}")
        
    # Load the environment variables
    load_dotenv(env_file)
    
    # Handle MongoDB URI variations
    if not os.getenv('MONGODB_URI') and os.getenv('MONGO_DB_URI'):
        os.environ['MONGODB_URI'] = os.getenv('MONGO_DB_URI')
    
    # Verify loaded variables
    required_vars = [
        'PINECONE_API_KEY',
        'OPENAI_API_KEY',
        'GROQ_API_KEY',
        'MONGODB_URI'
    ]
    
    print("\nChecking environment variables:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"{var}: {'*' * 5}{value[-5:] if value else 'Not Set'}")
        else:
            print(f"{var}: Not Set")
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

if __name__ == "__main__":
    load_environment()
