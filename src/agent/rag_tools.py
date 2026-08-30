from src.rag.retriever import FIRRetriever


class ShadowNetRAGTools:

    def __init__(self):

        self.retriever = FIRRetriever()

    def search_fir_evidence(
        self,
        query: str,
        top_k: int = 5
    ):

        return self.retriever.search(
            query=query,
            top_k=top_k
        )
