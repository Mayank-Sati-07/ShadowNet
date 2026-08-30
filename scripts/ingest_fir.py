"""
Small offline ingestion CLI to idempotently ingest FIRs into Pinecone using the
FIRIngestor class. This avoids any runtime embedding during API requests.

Usage:
    python scripts/ingest_fir.py /path/to/fir.txt FIR_ID

If run without args, will print usage.
"""

import sys
from src.rag.ingest import FIRIngestor


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/ingest_fir.py /path/to/fir.txt FIR_ID")
        return

    path = sys.argv[1]
    fir_id = sys.argv[2]

    ingestor = FIRIngestor()
    ingestor.ingest(path, fir_id)


if __name__ == '__main__':
    main()
