from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.document_loader import FIRDocumentLoader
from src.rag.vector_store import ShadowNetPineconeStore


class FIRIngestor:

    def __init__(self):

        self.store = ShadowNetPineconeStore()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def ingest(
        self,
        path: str,
        fir_id: str
    ):

        print("=" * 70)
        print("ShadowNet FIR PINECONE INGESTION")
        print("=" * 70)

        # =====================================================
        # 1. LOAD FIR
        # =====================================================

        print("\n[1] Loading FIR...")

        document = FIRDocumentLoader.load(
            path,
            fir_id
        )

        print(
            f"[OK] FIR loaded: {fir_id}"
        )

        print(
            f"[OK] Characters: "
            f"{len(document.page_content):,}"
        )

        # =====================================================
        # 2. CHUNK DOCUMENT
        # =====================================================

        print("\n[2] Creating chunks...")

        chunks = self.text_splitter.split_documents(
            [document]
        )

        print(
            f"[OK] Chunks created: {len(chunks)}"
        )

        # =====================================================
        # 3. CREATE EMBEDDINGS
        # =====================================================

        print("\n[3] Creating embeddings...")

        vectors = []

        for i, chunk in enumerate(chunks):

            text = chunk.page_content

            vector = self.store.embeddings.embed_query(
                text
            )

            vectors.append({
                "id": f"{fir_id}_chunk_{i}",

                "values": vector,

                "metadata": {
                    "fir_id": fir_id,
                    "chunk_id": i,
                    "text": text,
                    "source": path,
                    "document_type": "FIR"
                }
            })

        print(
            f"[OK] Embeddings created: {len(vectors)}"
        )

        if vectors:

            print(
                f"[OK] Vector dimension: "
                f"{len(vectors[0]['values'])}"
            )

        # =====================================================
        # 4. UPLOAD TO PINECONE
        # =====================================================

        print("\n[4] Uploading to Pinecone...")

        self.store.upsert(
            vectors
        )

        print(
            f"[OK] Uploaded {len(vectors)} vectors"
        )

        # =====================================================
        # 5. RESULT
        # =====================================================

        print("\n[OK] INGESTION COMPLETED")

        return vectors