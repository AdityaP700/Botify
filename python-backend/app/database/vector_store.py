from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings
from app.core.logger import logger

class VectorStore:
    def __init__(self):
        self.pc = None
        self.index = None
        self.init_pinecone()
    
    def init_pinecone(self):
        """
        Initialize Pinecone client and index.
        """
        try:
            # Initialize Pinecone
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Check if index exists
            existing_indexes = self.pc.list_indexes()
            
            # Create index if it doesn't exist
            if settings.PINECONE_INDEX_NAME not in existing_indexes:
                self.pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=1536,  # OpenAI text-embedding-3-small dimension
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-west-2")
                )
                logger.info(f"Created Pinecone index: {settings.PINECONE_INDEX_NAME}")
            
            # Get index
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
            logger.info("Successfully initialized Pinecone")
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            raise
    
    async def store_product_embedding(self, product_id: str, embedding: list, metadata: dict):
        """
        Store product embedding in Pinecone.
        """
        try:
            self.index.upsert(
                vectors=[{
                    "id": product_id,
                    "values": embedding,
                    "metadata": metadata
                }]
            )
            logger.info(f"Stored embedding for product: {product_id}")
        except Exception as e:
            logger.error(f"Error storing embedding: {e}")
            raise
    
    async def search_similar_products(self, query_embedding: list, top_k: int = 5):
        """
        Search for similar products using embedding.
        """
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            return results
        except Exception as e:
            logger.error(f"Error searching similar products: {e}")
            raise

vector_store = VectorStore()
