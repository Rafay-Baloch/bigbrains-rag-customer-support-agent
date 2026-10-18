import os
import json
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_FILE_PATH = os.path.join(BASE_DIR, 'knowledge_base.json')
CHROMA_DATA_PATH = os.path.join(BASE_DIR, 'chroma_db')

# 1. Initialize Persistent Chroma Client
chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

# Lightweight, accurate local embedding model
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

COLLECTION_NAME = "bigbrains_knowledge"

def get_or_create_collection():
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_func,
        metadata={"hnsw:space": "cosine"}
    )

def chunk_text(text, max_words=40):
    """Splits long text into meaningful semantic chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        if len(chunk.strip()) > 0:
            chunks.append(chunk)
    return chunks

def build_vector_database():
    """Reads knowledge_base.json, chunks content, generates embeddings, and saves into ChromaDB."""
    if not os.path.exists(KB_FILE_PATH):
        print(f"[!] Error: {KB_FILE_PATH} not found.")
        return

    with open(KB_FILE_PATH, 'r', encoding='utf-8') as f:
        kb_data = json.load(f)

    collection = get_or_create_collection()

    documents = []
    metadatas = []
    ids = []

    doc_index = 0
    print("\n[*] Initializing Embeddings & Vector Ingestion into ChromaDB...")

    for item in kb_data:
        category = item.get("category", "General")
        title = item.get("title", "")
        content = item.get("content", "")
        url = item.get("url", "")

        chunks = chunk_text(content)
        for chunk_idx, chunk in enumerate(chunks):
            chunk_id = f"doc_{doc_index}_chunk_{chunk_idx}"
            full_context = f"Title: {title} | Category: {category} | Info: {chunk}"
            
            documents.append(full_context)
            metadatas.append({
                "category": category,
                "title": title,
                "source_url": url,
                "chunk_index": chunk_idx
            })
            ids.append(chunk_id)

        doc_index += 1

    # Upsert into ChromaDB
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"[✓] Successfully embedded and stored {len(documents)} chunks into ChromaDB!")
    print(f"[✓] Vector Database persisted at: {CHROMA_DATA_PATH}\n")

def semantic_search(query, n_results=2, distance_threshold=0.65):
    """
    Searches most relevant context using cosine distance.
    Cosine distance range: 0.0 (identical) to 1.0+ (completely unrelated).
    Chunks with distance > distance_threshold are discarded to prevent hallucinations.
    """
    try:
        collection = get_or_create_collection()
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        matches = []
        if results and results.get("documents") and len(results["documents"][0]) > 0:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(docs)

            for i in range(len(docs)):
                dist = distances[i]
                # Filter out irrelevant chunks
                if dist <= distance_threshold:
                    matches.append({
                        "document": docs[i],
                        "metadata": metas[i],
                        "distance": dist
                    })
        return matches
    except Exception as e:
        print(f"[!] Semantic search error: {e}")
        return []

if __name__ == "__main__":
    build_vector_database()