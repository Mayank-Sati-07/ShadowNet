from src.graph.neo4j_client import Neo4jClient


client = Neo4jClient()

try:

    client.verify_connection()

finally:

    client.close()