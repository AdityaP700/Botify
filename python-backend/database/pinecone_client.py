import os
from pinecone import Pinecone, ServerlessSpec

def init_pinecone():
    # Create an instance of the Pinecone class
    pinecone_client = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

    index_name = "your_index_name"  # Make sure this matches your Pinecone setup

    # Check if the index exists, and if not, create it
    if index_name not in pinecone_client.list_indexes().names():
        pinecone_client.create_index(
            name=index_name,
            dimension=384,  # Adjust dimension based on your embedding model
            metric='cosine',  # Set metric as needed (e.g., 'cosine', 'euclidean', etc.)
            spec=ServerlessSpec(
                cloud="aws",   # or the cloud provider you are using
                region="us-west-2"  # or the specific region of your Pinecone project
            )
        )

    # Return the initialized Pinecone client and the index
    return pinecone_client, pinecone_client.Index(index_name)
