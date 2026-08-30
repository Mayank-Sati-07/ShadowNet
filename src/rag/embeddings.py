from langchain_huggingface import HuggingFaceEmbeddings

from src.rag.config import EMBEDDING_MODEL


class ShadowNetEmbeddings:

    def __init__(self):

        print(
            f"[Embeddings] Loading model: "
            f"{EMBEDDING_MODEL}"
        )

        self.model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        print("[OK] Embedding model loaded")

    def embed_documents(self, texts):

        return self.model.embed_documents(texts)

    def embed_query(self, text):

        return self.model.embed_query(text)

    def dimension(self):

        vector = self.embed_query(
            "ShadowNet criminal investigation"
        )

        return len(vector)
