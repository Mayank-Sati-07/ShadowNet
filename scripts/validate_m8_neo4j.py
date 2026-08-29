from src.graph.neo4j_client import Neo4jClient


def main():

    print("=" * 70)
    print("CNAS M8 NEO4J VALIDATION")
    print("=" * 70)

    client = Neo4jClient()

    # ============================================================
    # CONNECTION
    # ============================================================

    print("\n[1] Testing Neo4j connection...")

    client.verify_connection()

    # ============================================================
    # NODE COUNTS
    # ============================================================

    print("\n[2] Node counts")

    labels = [
        "FIR",
        "Person",
        "Location",
        "Organization",
        "Vehicle",
        "Phone",
        "Event"
    ]

    for label in labels:

        query = f"""
        MATCH (n:{label})
        RETURN count(n) AS count
        """

        records = client.execute_read(query)

        count = records[0]["count"]

        print(
            f"{label:15} : {count}"
        )

    # ============================================================
    # RELATIONSHIP COUNT
    # ============================================================

    print("\n[3] Relationship count")

    query = """
    MATCH ()-[r]->()
    RETURN count(r) AS count
    """

    records = client.execute_read(query)

    print(
        f"Total relationships : "
        f"{records[0]['count']}"
    )

    # ============================================================
    # RELATIONSHIP TYPES
    # ============================================================

    print("\n[4] Relationship types")

    query = """
    MATCH ()-[r]->()
    RETURN type(r) AS relationship,
           count(*) AS count
    ORDER BY count DESC
    """

    records = client.execute_read(query)

    for record in records:

        print(
            f"{record['relationship']:25} "
            f": {record['count']}"
        )

    # ============================================================
    # FIR CONNECTIONS
    # ============================================================

    print("\n[5] FIR -> entities")

    query = """
    MATCH (f:FIR)-[:MENTIONS]->(e)
    RETURN f.id AS fir,
           labels(e) AS entity_type,
           e.name AS name,
           e.registration_number AS vehicle,
           e.number AS phone
    ORDER BY fir
    """

    records = client.execute_read(query)

    for record in records:

        name = (
            record["name"]
            or record["vehicle"]
            or record["phone"]
        )

        print(
            f"{record['fir']} -> "
            f"{record['entity_type']} -> "
            f"{name}"
        )

    # ============================================================
    # COMPLETE GRAPH
    # ============================================================

    print("\n[6] Sample graph relationships")

    query = """
    MATCH (a)-[r]->(b)
    RETURN
        labels(a) AS source_type,
        a.name AS source_name,
        a.id AS source_id,
        type(r) AS relationship,
        labels(b) AS target_type,
        b.name AS target_name,
        b.id AS target_id
    LIMIT 50
    """

    records = client.execute_read(query)

    for record in records:

        source = (
            record["source_name"]
            or record["source_id"]
        )

        target = (
            record["target_name"]
            or record["target_id"]
        )

        print(
            f"{source} "
            f"--{record['relationship']}--> "
            f"{target}"
        )

    # ============================================================
    # CLOSE
    # ============================================================

    client.close()

    print("\n" + "=" * 70)
    print("✓ NEO4J VALIDATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()