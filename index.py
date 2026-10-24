"""Embed every chunk with bge-small-en-v1.5 and store it in a persistent ChromaDB collection.

Usage:
    python index.py   # (re)build chroma_db/ from documents/
"""

from functools import lru_cache
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks

MODEL_NAME = "BAAI/bge-small-en-v1.5"
DB_DIR = Path(__file__).parent / "chroma_db"
COLLECTION = "dsa_guide"
# bge v1.5 recommends this instruction on queries (not on passages) for retrieval.
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)


def get_collection():
    client = chromadb.PersistentClient(path=str(DB_DIR))
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def build_index(batch_size=1000):
    chunks = build_chunks()
    client = chromadb.PersistentClient(path=str(DB_DIR))
    if COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION)
    collection = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})

    print(f"Embedding {len(chunks)} chunks with {MODEL_NAME} ...")
    embeddings = get_model().encode(
        [c["text"] for c in chunks], batch_size=32, normalize_embeddings=True, show_progress_bar=True
    )
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        collection.add(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            embeddings=embeddings[i:i + batch_size].tolist(),
            metadatas=[c["metadata"] for c in batch],
        )
    print(f"Stored {collection.count()} chunks in {DB_DIR}/{COLLECTION}")


if __name__ == "__main__":
    build_index()
