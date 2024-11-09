from sentence_transformers import SentenceTransformer
from database.mongo_client import get_data_from_mongo
from database.pinecone_client import upsert_to_pinecone

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_and_store():
    data = get_data_from_mongo()
    pinecone_data = []

    for item in data:
        doc_id = str(item["_id"])
        description = item["description"]
        embedding = model.encode(description).tolist()
        pinecone_data.append((doc_id, embedding, {"description": description}))

    upsert_to_pinecone(pinecone_data)
