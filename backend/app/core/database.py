import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
)


def verify_database():
    driver.verify_connectivity()


def execute_query(query: str, parameters: dict | None = None):
    records, summary, keys = driver.execute_query(
        query,
        parameters_=parameters or {},
        database_=NEO4J_DATABASE,
    )

    return [record.data() for record in records]