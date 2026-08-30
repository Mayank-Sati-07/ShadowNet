import os


# ============================================================
# PINECONE
# ============================================================

PINECONE_INDEX_NAME = "cnas-fir-index"

PINECONE_DIMENSION = 1024

PINECONE_METRIC = "cosine"

PINECONE_NAMESPACE = "fir-documents"


# ============================================================
# EMBEDDINGS
# ============================================================

EMBEDDING_MODEL = "BAAI/bge-m3"


# ============================================================
# CHUNKING
# ============================================================

CHUNK_SIZE = 700

CHUNK_OVERLAP = 100


# ============================================================
# ENVIRONMENT
# ============================================================

from src.config import settings

PINECONE_API_KEY = settings.pinecone_api_key