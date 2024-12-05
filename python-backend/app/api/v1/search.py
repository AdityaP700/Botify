from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from database.pinecone_client import index
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

class SearchResult(BaseModel):
    score: float
    text: str

@router.post("/search", response_model=list[SearchResult])
async def semantic_search(search_query: SearchQuery):
    """
    Perform semantic search on the product database
    """
    try:
        # Generate embedding for the query
        query_embedding = model.encode(search_query.query).tolist()
        
        # Search in Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=search_query.top_k,
            include_metadata=True
        )
        
        # Format results
        formatted_results = [
            SearchResult(
                score=match.score,
                text=match.metadata.get('text', 'No text available')
            )
            for match in results.matches
        ]
        
        return formatted_results
    
    except Exception as e:
        logger.error(f"Error during semantic search: {e}")
        raise HTTPException(status_code=500, detail=str(e))
