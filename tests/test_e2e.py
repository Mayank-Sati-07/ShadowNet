from fastapi.testclient import TestClient

from src.api.main import app
from src.rag.ingest import FIRIngestor
import os


client = TestClient(app)


def test_api_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"


def test_dry_run_ingest_creates_vectors(tmp_path):
    # Use the sample FIR file included in the repository
    sample = os.path.join("data", "documents", "sample_fir.txt")
    assert os.path.exists(sample), "sample FIR file missing"

    ingestor = FIRIngestor()
    vectors = ingestor.ingest(sample, "SAMPLE_FIR_TEST", dry_run=True)

    # Should return a list of vectors in dry-run mode
    assert isinstance(vectors, list)
    assert len(vectors) > 0

    # Each vector should have expected keys
    v = vectors[0]
    assert "id" in v and "values" in v and "metadata" in v
