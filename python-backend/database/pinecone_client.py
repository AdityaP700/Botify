import os
from pinecone import Pinecone, ServerlessSpec
import logging
import sys
from pathlib import Path

# Add parent directory to Python path to import load_env
sys.path.append(str(Path(__file__).parent.parent))
from load_env import load_environment

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pinecone client
def init_pinecone():
    try:
        # Load environment variables
        load_environment()
        
        # Get environment variables
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable not set")

        # Create an instance of the Pinecone class
        pinecone_client = Pinecone(api_key=api_key)
        
        # Index configuration
        INDEX_NAME = "botify-index"
        DIMENSION = 384  # dimension for all-MiniLM-L6-v2 model
        METRIC = "cosine"

        # List existing indexes
        existing_indexes = [index.name for index in pinecone_client.list_indexes()]
        
        # Check if index exists
        if INDEX_NAME in existing_indexes:
            # Get index info
            index_info = pinecone_client.describe_index(INDEX_NAME)
            
            # Check if dimensions match
            if index_info.dimension != DIMENSION:
                logger.info(f"Deleting index {INDEX_NAME} due to dimension mismatch")
                pinecone_client.delete_index(INDEX_NAME)
                
                # Create new index with correct dimensions
                logger.info(f"Creating new index {INDEX_NAME} with dimension {DIMENSION}")
                pinecone_client.create_index(
                    name=INDEX_NAME,
                    dimension=DIMENSION,
                    metric=METRIC,
                    spec={
                        "pod": {
                            "environment": "gcp-starter",
                            "pod_type": "starter"
                        }
                    }
                )
        else:
            # Create new index
            logger.info(f"Creating new index {INDEX_NAME}")
            pinecone_client.create_index(
                name=INDEX_NAME,
                dimension=DIMENSION,
                metric=METRIC,
                spec={
                    "pod": {
                        "environment": "gcp-starter",
                        "pod_type": "starter"
                    }
                }
            )
        
        # Get index
        index = pinecone_client.Index(INDEX_NAME)
        stats = index.describe_index_stats()
        logger.info(f"Successfully connected to Pinecone index '{INDEX_NAME}'. Vector count: {stats.total_vector_count}")
        
        return index

    except Exception as e:
        logger.error(f"Error initializing Pinecone: {e}")
        raise

def test_pinecone_operations(index):
    """Test Pinecone operations with sample data."""
    try:
        # Test data
        test_vectors = [
            {
                "id": "test1",
                "values": [0.1] * 384,  # dimension for all-MiniLM-L6-v2 model
                "metadata": {"text": "This is a test product description"}
            },
            {
                "id": "test2",
                "values": [0.2] * 384,
                "metadata": {"text": "Another test product description"}
            }
        ]

        # Upsert test vectors
        index.upsert(vectors=test_vectors)
        logger.info("Successfully upserted test vectors")

        # Query test
        query_response = index.query(
            vector=[0.1] * 384,
            top_k=2,
            include_values=True,
            include_metadata=True
        )
        logger.info(f"Query response: {query_response}")

        return True

    except Exception as e:
        logger.error(f"Error testing Pinecone operations: {str(e)}")
        return False

# Initialize Pinecone when the module is imported
try:
    index = init_pinecone()
    # Uncomment the following line to test operations
    # test_success = test_pinecone_operations(index)
except Exception as e:
    logger.error(f"Failed to initialize Pinecone index: {str(e)}")
    raise

if __name__ == "__main__":
    # Test the Pinecone connection and operations
    test_success = test_pinecone_operations(index)
    if test_success:
        print(" Pinecone connection and operations test successful!")
    else:
        print(" Pinecone test failed. Check the logs for details.")
