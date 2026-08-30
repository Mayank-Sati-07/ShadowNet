from src.rag.rag_pipeline import FIRRAGPipeline


def main():

    print("=" * 70)
    print("CNAS RAG INVESTIGATION TEST")
    print("=" * 70)

    pipeline = FIRRAGPipeline()

    question = (
        "How is Raj Kumar connected "
        "to Amit Sharma?"
    )

    result = pipeline.ask(
        question=question,
        top_k=5
    )

    print("\n" + "=" * 70)
    print("INVESTIGATION ANSWER")
    print("=" * 70)

    print(
        result["answer"]
    )

    print("\n" + "=" * 70)
    print("EVIDENCE")
    print("=" * 70)

    for i, evidence in enumerate(
        result["evidence"],
        start=1
    ):

        print(
            f"\n[{i}] "
            f"{evidence['fir_id']} "
            f"| score={evidence['score']:.4f}"
        )

        print(
            evidence["text"]
        )


if __name__ == "__main__":
    main()