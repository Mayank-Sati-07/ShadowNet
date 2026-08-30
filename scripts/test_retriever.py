from src.rag.retriever import FIRRetriever
from dotenv import load_dotenv

load_dotenv()

def main():

    print("=" * 70)
    print("CNAS RAG RETRIEVAL")
    print("=" * 70)

    retriever = FIRRetriever()

    query = (
        "How is Raj Kumar connected "
        "to Amit Sharma?"
    )

    results = retriever.search(
        query=query,
        top_k=5
    )

    print(
        f"\n✓ Results returned: "
        f"{len(results)}"
    )

    print("\n" + "=" * 70)
    print("RETRIEVED EVIDENCE")
    print("=" * 70)

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n[{i}] "
            f"Score: {result['score']:.4f}"
        )

        print(
            f"FIR: {result['fir_id']}"
        )

        print(
            f"Chunk: {result['chunk_id']}"
        )

        print(
            f"Text:\n{result['text']}"
        )


if __name__ == "__main__":
    main()