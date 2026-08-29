from src.graph.neo4j_client import Neo4jClient


QUERIES = {

    "Total Nodes": """
        MATCH (n)
        RETURN count(n) AS count
    """,

    "Total Relationships": """
        MATCH ()-[r]->()
        RETURN count(r) AS count
    """,

    "Persons": """
        MATCH (n:Person)
        RETURN count(n) AS count
    """,

    "Phones": """
        MATCH (n:Phone)
        RETURN count(n) AS count
    """,

    "Vehicles": """
        MATCH (n:Vehicle)
        RETURN count(n) AS count
    """,

    "Locations": """
        MATCH (n:Location)
        RETURN count(n) AS count
    """,

    "Organizations": """
        MATCH (n:Organization)
        RETURN count(n) AS count
    """,

    "Accounts": """
        MATCH (n:Account)
        RETURN count(n) AS count
    """,

    "FIRs": """
        MATCH (n:FIR)
        RETURN count(n) AS count
    """,

    "Police Stations": """
        MATCH (n:PoliceStation)
        RETURN count(n) AS count
    """,

    "Crimes": """
        MATCH (n:Crime)
        RETURN count(n) AS count
    """,

    "Statutes": """
        MATCH (n:Statute)
        RETURN count(n) AS count
    """,

    "Calls": """
        MATCH ()-[r:CALLED]->()
        RETURN count(r) AS count
    """,

    "Emails": """
        MATCH ()-[r:EMAILED]->()
        RETURN count(r) AS count
    """,

    "Transactions": """
        MATCH ()-[r:TRANSFERRED_MONEY]->()
        RETURN count(r) AS count
    """,

    "Visits": """
        MATCH ()-[r:VISITED]->()
        RETURN count(r) AS count
    """,

    "FIR → PoliceStation": """
        MATCH ()-[r:FILED_AT]->()
        RETURN count(r) AS count
    """,

    "FIR → Crime": """
        MATCH ()-[r:ABOUT_CRIME]->()
        RETURN count(r) AS count
    """,

    "Crime → Statute": """
        MATCH ()-[r:UNDER_STATUTE]->()
        RETURN count(r) AS count
    """
}


def run_count_query(client, query):
    """
    Execute a count query using the current Neo4jClient.

    Neo4jClient.execute() returns a ResultSummary,
    so we cannot use result.single().
    """

    with client.driver.session() as session:

        result = session.run(query)

        record = result.single()

        return record["count"]


def main():

    client = Neo4jClient()

    try:

        client.verify_connection()

        print()
        print("CNAS GRAPH VALIDATION")
        print("=" * 60)

        total_nodes = 0
        total_relationships = 0

        for name, query in QUERIES.items():

            count = run_count_query(
                client,
                query
            )

            print(
                f"{name:<30} {count:>10,}"
            )

            if name == "Total Nodes":
                total_nodes = count

            elif name == "Total Relationships":
                total_relationships = count

        print("=" * 60)

        print(
            f"Total nodes verified: "
            f"{total_nodes:,}"
        )

        print(
            f"Total relationships verified: "
            f"{total_relationships:,}"
        )

        print()
        print("✓ CNAS graph validation completed")

    finally:

        client.close()


if __name__ == "__main__":
    main()