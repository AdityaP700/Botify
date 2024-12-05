import os
import sys
from pathlib import Path
import logging

# Add the parent directory to the Python path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

from sentence_transformers import SentenceTransformer
from database.mongo_client import get_data_from_mongo
from database.pinecone_client import index

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """Get embedding for a given text using sentence-transformers"""
    try:
        # Generate embedding
        embedding = model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None

def transfer_data_to_pinecone():
    """Transfer data from MongoDB to Pinecone"""
    logger.info("Fetching data from MongoDB...")
    mongo_data = get_data_from_mongo()
    
    if not mongo_data:
        logger.info("No data found in MongoDB!")
        return
    
    logger.info(f"Found {len(mongo_data)} documents in MongoDB")
    
    # Process each document
    for i, doc in enumerate(mongo_data):
        try:
            # Get the description text from MongoDB document
            text = doc.get('description', '')
            if not text:
                logger.warning(f"Skipping document {doc['_id']} - no description found")
                continue
            
            # Generate embedding for the text
            embedding = get_embedding(text)
            if not embedding:
                logger.warning(f"Skipping document {doc['_id']} - embedding generation failed")
                continue
            
            # Prepare metadata
            metadata = {
                'mongo_id': str(doc['_id']),
                'text': text[:1000]  # Store first 1000 chars of text in metadata
            }
            
            # Upload to Pinecone
            index.upsert(
                vectors=[{
                    'id': f'mongo_{str(doc["_id"])}',
                    'values': embedding,
                    'metadata': metadata
                }]
            )
            
            logger.info(f"Processed document {i + 1}/{len(mongo_data)}")
            
        except Exception as e:
            logger.error(f"Error processing document {doc.get('_id', i)}: {e}")
            continue

if __name__ == "__main__":
    logger.info("Starting data transfer from MongoDB to Pinecone...")
    transfer_data_to_pinecone()
    logger.info("Data transfer complete!")
