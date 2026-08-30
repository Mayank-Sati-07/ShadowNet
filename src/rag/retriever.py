from src.rag.vector_store import CNASPineconeStore
from src.config import settings


class FIRRetriever:

    def __init__(self):
        # Use query-only store in runtime to avoid loading embedding models
        self.store = CNASPineconeStore(mode="query")

    # =========================================================
    # SEARCH
    # =========================================================

    def search(
        self,
        query: str,
        top_k: int = 5,
        fir_id: str | None = None
    ):

        print(f"\n[RAG] Query: {query}")

        # -----------------------------------------------------
        # 1. EMBED QUESTION
        # -----------------------------------------------------

        if not settings.allow_runtime_embeddings:
            raise RuntimeError(
                "Runtime embedding is disabled. Please run offline ingestion to populate vectors."
            )

        # If allowed (development), ensure store has embeddings loaded
        if not self.store.embeddings:
            self.store = CNASPineconeStore(mode="ingest")

        query_vector = self.store.embeddings.embed_query(query)

        # -----------------------------------------------------
        # 2. PINECONE SEARCH
        # -----------------------------------------------------

        matches = self.store.query(
            query_vector=query_vector,
            top_k=top_k,
            fir_id=fir_id
        )

        # -----------------------------------------------------
        # 3. CLEAN RESULTS
        # -----------------------------------------------------

        results = []

        for match in matches:
            metadata = match.metadata or {}
            results.append({
                "id": match.id,
                "score": float(match.score),
                "fir_id": metadata.get("fir_id"),
                "chunk_id": metadata.get("chunk_id"),
                "text": metadata.get("text", ""),
                "source": metadata.get("source"),
                "document_type": metadata.get("document_type", "FIR"),
            })

        return results