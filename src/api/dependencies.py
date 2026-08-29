from functools import lru_cache

from src.graph.neo4j_client import Neo4jClient
from src.graph.investigation_service import GraphInvestigationService
from src.agent.graph import CNASInvestigationAgent


@lru_cache()
def get_neo4j_client() -> Neo4jClient:
    client = Neo4jClient()
    client.verify_connection()
    return client


@lru_cache()
def get_graph_service() -> GraphInvestigationService:
    return GraphInvestigationService()


@lru_cache()
def get_investigation_agent() -> CNASInvestigationAgent:
    return CNASInvestigationAgent()