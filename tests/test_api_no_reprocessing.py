import os

import pytest

from fastapi.testclient import TestClient

from src.api.main import app


def test_get_persons_no_rag_init(monkeypatch):
    # Ensure that creating the TestClient and calling /api/persons does not trigger heavy RAG initialization
    # We monkeypatch FIRRAGPipeline to raise if instantiated
    import src.rag.rag_pipeline as rp

    def fail_init(*args, **kwargs):
        raise RuntimeError("RAG pipeline must not be initialized during lightweight API calls")

    monkeypatch.setattr(rp, "FIRRAGPipeline", fail_init)

    client = TestClient(app)
    r = client.get("/api/persons")
    assert r.status_code == 200
