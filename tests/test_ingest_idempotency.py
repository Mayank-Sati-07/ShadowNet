import os
import json
from pathlib import Path

import pytest

from src.rag import registry


class DummyStore:
    def __init__(self, mode="ingest"):
        class E:
            def embed_query(self, text):
                return [0.0] * 1024

        self.embeddings = E() if mode == "ingest" else None
        self.upserted = []

    def upsert(self, vectors):
        self.upserted.extend(vectors)


@pytest.fixture(autouse=True)
def set_registry_db(tmp_path, monkeypatch):
    db_path = tmp_path / "registry.db"
    monkeypatch.setenv("CNAS_REGISTRY_DB", str(db_path))
    # Ensure registry module uses this path
    registry.init_db()
    yield


def test_ingest_idempotent(monkeypatch, tmp_path):
    # Monkeypatch the vector store class used in ingest to avoid external calls
    import importlib

    monkeypatch.setenv("PINECONE_API_KEY", "test-key")

    # Replace CNASPineconeStore in the ingest module
    import src.rag.ingest as ingest_mod

    monkeypatch.setattr(ingest_mod, "CNASPineconeStore", lambda mode="ingest": DummyStore(mode=mode))

    # Create a fake document loader that returns a simple object
    class Doc:
        def __init__(self, text):
            self.page_content = text

    monkeypatch.setattr(ingest_mod, "FIRDocumentLoader", type("L", (), {"load": staticmethod(lambda p, fid: Doc("hello world"))}))

    ingestor = ingest_mod.FIRIngestor()

    # First ingest should process and create chunks
    chunks1 = ingestor.ingest("path/to/doc.txt", "DOC_1")
    assert isinstance(chunks1, list)

    # Second ingest with same content should be skipped and return the same chunk list
    chunks2 = ingestor.ingest("path/to/doc.txt", "DOC_1")
    assert chunks1 == chunks2

    # Registry should contain document
    doc = registry.get_document("DOC_1")
    assert doc is not None
    assert doc["document_id"] == "DOC_1"
