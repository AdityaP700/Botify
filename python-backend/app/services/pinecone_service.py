from pinecone import Pinecone, PodSpec
from app.core.config import settings
from app.core.logger import logger
from typing import List, Dict, Any

class PineconeService:
    def __init__(self):
        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index_name = "botify-products"
            self._ensure_index_exists()
            logger.info("Pinecone service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {str(e)}")
            raise

    def _ensure_index_exists(self):
        """Ensure the required index exists, create if it doesn't"""
        try:
            # List all indexes
            indexes = self.pc.list_indexes()
            
            # Create index if it doesn't exist
            if self.index_name not in indexes:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI embeddings dimension
                    metric="cosine",
                    spec=PodSpec(
                        environment="gcp-starter"
                    )
                )
                logger.info(f"Created new Pinecone index: {self.index_name}")
            
            # Get the index
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
        
        except Exception as e:
            logger.error(f"Error ensuring index exists: {str(e)}")
            raise

    async def search_similar_products(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar products using vector embeddings"""
        try:
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True
            )
            return results.matches
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return []

    async def store_product(self, product_id: str, vector: List[float], metadata: Dict[str, Any]):
        """Store a product embedding and metadata"""
        try:
            self.index.upsert(
                vectors=[{
                    "id": product_id,
                    "values": vector,
                    "metadata": metadata
                }]
            )
            logger.info(f"Stored product {product_id} in Pinecone")
        except Exception as e:
            logger.error(f"Error storing product: {str(e)}")
            raise
