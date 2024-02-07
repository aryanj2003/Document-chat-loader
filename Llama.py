from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from torch import cuda

embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

embed_model = HuggingFaceEmbeddings(
    model_name=embed_model_id,
    model_kwargs={'device': device},
    encode_kwargs={'device': device, 'batch_size': 32}
)

docs = [
    "this is one document",
    "and another document"
]

embeddings = embed_model.embed_documents(docs)

print(f"We have {len(embeddings)} doc embeddings, each with "
      f"a dimensionality of {len(embeddings[0])}.")

import os
import time

from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="79f47e3f-6b72-4b15-84bc-10e43d193d74") # This reads the PINECONE_API_KEY env var

# # get API key from app.pinecone.io and environment from console
# pinecone.init(
#     api_key=os.environ.get('PINECONE_API_KEY') or 'PINECONE_API_KEY',
#     environment=os.environ.get('PINECONE_ENVIRONMENT') or 'gcp-starter'
# )



index_name = 'llama-2-rag'

try:

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            index_name,
            dimension=len(embeddings[0]),
            metric='cosine',
            spec=ServerlessSpec(cloud="aws", region="us-west-2")
        )
        # wait for index to finish initialization
        while not pinecone.describe_index(index_name).status['ready']:
            time.sleep(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")