from src.rag.ingest import FIRIngestor
from dotenv import load_dotenv
load_dotenv()

def main():

    print("=" * 70)
    print("CNAS PINECONE INGESTION TEST")
    print("=" * 70)

    path = "data/documents/raw/sample_fir.txt"

    fir_id = "FIR-2026-0001"

    ingestor = FIRIngestor()

    vectors = ingestor.ingest(
        path=path,
        fir_id=fir_id
    )

    print("\n" + "=" * 70)
    print("INGESTION RESULT")
    print("=" * 70)

    print(
        f"FIR: {fir_id}"
    )

    print(
        f"Vectors uploaded: {len(vectors)}"
    )

    if vectors:

        print(
            f"Vector dimension: "
            f"{len(vectors[0]['values'])}"
        )

        print("\nFirst vector metadata:")

        print(
            vectors[0]["metadata"]
        )


if __name__ == "__main__":
    main()