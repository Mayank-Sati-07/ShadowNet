import pandas as pd

from src.graph.neo4j_client import Neo4jClient


def save_anomalies(df):

    client = Neo4jClient()

    try:

        client.verify_connection()

        rows = df.to_dict(
            orient="records"
        )

        query = """
        UNWIND $rows AS row

        MERGE (
            t:Transaction {
                transaction_id:
                    row.transaction_id
            }
        )

        SET
            t.amount = row.amount,
            t.timestamp = row.timestamp,
            t.anomaly_score =
                row.anomaly_score,
            t.is_anomaly =
                row.is_anomaly,
            t.reason =
                row.reason

        WITH t, row

        MATCH (
            p:Person {
                person_id:
                    row.person_id
            }
        )

        MERGE (
            p)-[:MADE_TRANSACTION]->(t)
        """

        client.execute(
            query,
            {
                "rows": rows
            }
        )

        print(
            f"[OK] Saved {len(rows):,} "
            f"transactions to Neo4j"
        )

    finally:

        client.close()