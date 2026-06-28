from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

VECTOR_DB = BASE_DIR / "vector_db" / "faiss_index"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 250

TOP_K = 8

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

OLLAMA_MODEL = "qwen3:4b"