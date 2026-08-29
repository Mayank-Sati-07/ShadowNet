import os

from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings


class CNASPineconeStore:

    INDEX_NAME = "cnas-fir-index"
    EXPECTED_DIMENSION = 1024

    def __init__(self):

        print(
            "[Embeddings] Loading model: BAAI/bge-m3"
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        print("✓ Embedding model loaded")

        # Verify dimension
        test_vector = self.embeddings.embed_query(
            "CNAS FIR investigation"
        )

        dimension = len(test_vector)

        print(
            f"✓ Embedding dimension: {dimension}"
        )

        if dimension != self.EXPECTED_DIMENSION:
            raise ValueError(
                f"Expected embedding dimension "
                f"{self.EXPECTED_DIMENSION}, "
                f"got {dimension}"
            )

        api_key = os.getenv("PINECONE_API_KEY")

        if not api_key:
            raise ValueError(
                "PINECONE_API_KEY is missing"
            )

        self.pc = Pinecone(
            api_key=api_key
        )

        self.index = self.pc.Index(
            self.INDEX_NAME
        )

        print(
            f"✓ Pinecone index connected: "
            f"{self.INDEX_NAME}"
        )

    # =========================================================
    # UPSERT
    # =========================================================

    def upsert(self, vectors):

        if not vectors:
            return

        self.index.upsert(
            vectors=vectors
        )

    # =========================================================
    # QUERY
    # =========================================================

    def query(
        self,
        query_vector,
        top_k=5,
        fir_id=None
    ):

        kwargs = {
            "vector": query_vector,
            "top_k": top_k,
            "include_metadata": True
        }

        if fir_id:
            kwargs["filter"] = {
                "fir_id": {
                    "$eq": fir_id
                }
            }

        response = self.index.query(
            **kwargs
        )

        return response.matches