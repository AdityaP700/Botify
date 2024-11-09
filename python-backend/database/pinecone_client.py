import  os
from pinecone import Pinecone, ServerlessSpec

def init_pinecone():
    pinecone_client = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

    index_name = "your_index_name"  

    if index_name not in pinecone_client.list_indexes().names():
        pinecone_client.create_index(
            name=index_name,
            dimension=384,  
            metric='cosine',  
            spec=ServerlessSpec(
                cloud="aws",   
                region="us-west-2"  
            )
        )

    return pinecone_client, pinecone_client.Index(index_name)
