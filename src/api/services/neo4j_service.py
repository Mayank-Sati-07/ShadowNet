from neo4j import GraphDatabase
import os


class Neo4jService:

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "cnas_password")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def close(self):
        self.driver.close()

    def execute(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(
                query,
                parameters or {}
            )
            return [record.data() for record in result]