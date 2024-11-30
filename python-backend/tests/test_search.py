import sys
from pathlib import Path
import logging

# Add the parent directory to the Python path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

from sentence_transformers import SentenceTransformer
from database.pinecone_client import index

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_search(query, top_k=3):
    """
    Perform semantic search using the given query.
    
    Args:
        query (str): The search query
        top_k (int): Number of results to return
    
    Returns:
        list: List of search results with scores and texts
    """
    try:
        # Generate embedding for the query
        query_embedding = model.encode(query).tolist()
        
        # Search in Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        return results.matches
    
    except Exception as e:
        logger.error(f"Error during semantic search: {e}")
        return []

def print_results(results):
    """Print search results in a formatted way"""
    print("\nSearch Results:")
    print("-" * 80)
    for i, match in enumerate(results, 1):
        print(f"{i}. Score: {match.score:.3f}")
        print(f"   Text: {match.metadata.get('text', 'No text')}")
        print("-" * 80)

def interactive_search():
    """Interactive search function"""
    print("\nWelcome to Semantic Search Testing!")
    print("Enter your search queries below (type 'exit' to quit)")
    print("-" * 80)
    
    while True:
        query = input("\nEnter your search query: ").strip()
        
        if query.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not query:
            print("Please enter a valid query")
            continue
        
        results = semantic_search(query)
        print_results(results)

if __name__ == "__main__":
    interactive_search()
