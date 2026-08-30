import os

from dotenv import load_dotenv
from pinecone import Pinecone


def main():

    load_dotenv()

    print("=" * 70)
    print("PINECONE CONNECTION TEST")
    print("=" * 70)

    api_key = os.getenv("PINECONE_API_KEY")

    if not api_key:
        raise ValueError(
            "PINECONE_API_KEY is missing"
        )

    print("✓ Pinecone API key loaded")

    pc = Pinecone(
        api_key=api_key
    )

    indexes = pc.list_indexes()

    print("\nAvailable indexes:")

    for index in indexes:
        print(
            f"  - {index.name}"
        )

    index_name = os.getenv(
        "PINECONE_INDEX_NAME",
        "cnas-fir-index"
    )

    if index_name not in indexes.names():

        raise ValueError(
            f"Index '{index_name}' not found"
        )

    print(
        f"\n✓ Index found: {index_name}"
    )

    index = pc.Index(index_name)

    description = index.describe_index_stats()

    print("\nIndex statistics:")
    print(description)

    print("\n✓ PINECONE CONNECTION TEST PASSED")


if __name__ == "__main__":
    main()