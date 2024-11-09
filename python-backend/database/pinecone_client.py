import pinecone
from config.pinecone_config import init_pinecone

def upsert_to_pinecone(data):
    init_pinecone()
    index_name = "your_index_name"  # Ensure this index is created in Pinecone

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=384)  # Adjust dimension as per embedding model

    index = pinecone.Index(index_name)
    index.upsert(vectors=data)
