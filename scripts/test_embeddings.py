from src.rag.embeddings import CNASEmbeddings
from src.rag.config import PINECONE_DIMENSION


def main():

    print("=" * 70)
    print("CNAS EMBEDDING TEST")
    print("=" * 70)

    embeddings = CNASEmbeddings()

    vector = embeddings.embed_query(
        "Raj Kumar met Amit Sharma."
    )

    dimension = len(vector)

    print(
        f"\nEmbedding dimension: {dimension}"
    )

    print(
        f"Expected Pinecone dimension: "
        f"{PINECONE_DIMENSION}"
    )

    if dimension != PINECONE_DIMENSION:

        raise ValueError(
            f"Dimension mismatch: "
            f"{dimension} != "
            f"{PINECONE_DIMENSION}"
        )

    print(
        "\n✓ Embedding dimension matches Pinecone"
    )


if __name__ == "__main__":
    main()
