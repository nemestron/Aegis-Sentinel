import os
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Disable telemetry and set database path
db_path = os.path.join(os.getcwd(), "local_db")
client = chromadb.PersistentClient(path=db_path, settings=Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection(name="aegis_memory")

# Initialize Local Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def ingest_data(text: str, url: str):
    """Chunks text, embeds it, and stores it in ChromaDB with source URLs."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    
    if not chunks:
        return

    ids = [f"{url}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": url} for _ in range(len(chunks))]
    
    # Embed and upsert
    embeds = embeddings.embed_documents(chunks)
    collection.upsert(
        documents=chunks,
        embeddings=embeds,
        metadatas=metadatas,
        ids=ids
    )

def search_memory(query: str, n_results: int = 3) -> dict:
    """Performs semantic search and returns documents and metadata."""
    query_embed = embeddings.embed_query(query)
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=n_results
    )
    return results