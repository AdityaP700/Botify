import json
import os
from openai import OpenAI
from database.pinecone_client import index

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embedding(text):
    """Get embedding for a given text using OpenAI's API"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def load_qa_pairs():
    """Load Q&A pairs from JSON file"""
    with open('python-backend/data/sample_qa.json', 'r') as file:
        data = json.load(file)
    return data['qa_pairs']

def upload_to_pinecone():
    """Process Q&A pairs and upload to Pinecone"""
    qa_pairs = load_qa_pairs()
    
    # Process each Q&A pair
    for i, pair in enumerate(qa_pairs):
        # Combine question and answer for context
        combined_text = f"Question: {pair['question']}\nAnswer: {pair['answer']}"
        
        # Get embedding for the combined text
        embedding = get_embedding(combined_text)
        
        # Prepare metadata
        metadata = {
            'question': pair['question'],
            'answer': pair['answer']
        }
        
        # Upload to Pinecone
        index.upsert(
            vectors=[{
                'id': f'qa_pair_{i}',
                'values': embedding,
                'metadata': metadata
            }]
        )
        print(f"Uploaded Q&A pair {i + 1}/{len(qa_pairs)}")

if __name__ == "__main__":
    print("Starting data upload to Pinecone...")
    upload_to_pinecone()
    print("Data upload complete!")
