from src.rag.retriever import FIRRetriever
from src.rag.answer_generator import FIRAnswerGenerator


class FIRRAGPipeline:

    def __init__(self):

        self.retriever = FIRRetriever()

        self.generator = (
            FIRAnswerGenerator()
        )

    def ask(
        self,
        question: str,
        top_k: int = 5,
        fir_id: str | None = None
    ):

        print(
            "\n[RAG] Retrieving evidence..."
        )

        evidence = self.retriever.search(
            query=question,
            top_k=top_k,
            fir_id=fir_id
        )

        print(
            f"✓ Retrieved {len(evidence)} "
            f"evidence chunks"
        )

        print(
            "\n[RAG] Generating answer..."
        )

        answer = self.generator.generate(
            question=question,
            evidence=evidence
        )

        print(
            "✓ Answer generated"
        )

        return {
            "question": question,
            "answer": answer,
            "evidence": evidence
        }