import os

import pytest
from dotenv import load_dotenv

load_dotenv()


def _has_neo4j_credentials() -> bool:
    return all(
        os.getenv(name)
        for name in ("NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD")
    )


def _has_pinecone_credentials() -> bool:
    return bool(os.getenv("PINECONE_API_KEY"))


@pytest.mark.integration
def test_neo4j_connection_and_basic_query():
    if not _has_neo4j_credentials():
        pytest.skip("Neo4j credentials are not configured; set NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD to run this integration test.")

    from src.graph.neo4j_client import Neo4jClient

    client = Neo4jClient()
    if not client.verify_connection():
        pytest.skip("Neo4j service is not reachable at the configured URI.")

    rows = client.execute_read("RETURN 1 AS value")
    assert rows, "Neo4j query returned no rows"
    assert rows[0]["value"] == 1


@pytest.mark.integration
def test_pinecone_index_stats_are_accessible():
    if not _has_pinecone_credentials():
        pytest.skip("Pinecone credentials are not configured; set PINECONE_API_KEY to run this integration test.")

    from src.rag.vector_store import CNASPineconeStore

    store = CNASPineconeStore(mode="query")
    stats = store.index.describe_index_stats()

    if stats is None:
        pytest.skip("Pinecone index stats were unavailable from the configured service.")

    payload = None
    if isinstance(stats, dict):
        payload = stats
    else:
        payload = getattr(stats, "_data_store", None)
        if payload is None:
            model_dump = getattr(type(stats), "model_dump", None)
            if callable(model_dump):
                try:
                    payload = model_dump(stats)
                except TypeError:
                    payload = model_dump()
            if payload is None:
                payload = getattr(stats, "__dict__", {})
                if isinstance(payload, dict) and "_data_store" in payload:
                    payload = payload["_data_store"]

    if not payload:
        pytest.skip("Pinecone index stats payload was empty from the configured service.")

    if hasattr(payload, "items"):
        payload = dict(payload)

    assert "total_vector_count" in payload
    assert isinstance(payload["total_vector_count"], int)
