import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


class Neo4jClient:

    def __init__(self):

        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        if not uri:
            raise ValueError("NEO4J_URI is missing")

        if not username:
            raise ValueError("NEO4J_USERNAME is missing")

        if not password:
            raise ValueError("NEO4J_PASSWORD is missing")

        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

    def verify_connection(self):

        self.driver.verify_connectivity()

        print("✓ Neo4j connection successful")

    def execute(self, query, parameters=None):

        """
        Execute a write/query operation.

        Returns ResultSummary.
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                parameters or {}
            )

            return result.consume()

    def execute_read(self, query, parameters=None):

        """
        Execute a read query and return all records.
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                parameters or {}
            )

            return list(result)

    def execute_write(self, query, parameters=None):

        """
        Execute a write query.
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                parameters or {}
            )

            return result.consume()

    def close(self):

        self.driver.close()