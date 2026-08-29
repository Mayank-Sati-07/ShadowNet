from src.graph.neo4j_client import Neo4jClient


CONSTRAINTS = [

    """
    CREATE CONSTRAINT person_id_unique IF NOT EXISTS
    FOR (p:Person)
    REQUIRE p.person_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT phone_id_unique IF NOT EXISTS
    FOR (p:Phone)
    REQUIRE p.phone_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT vehicle_id_unique IF NOT EXISTS
    FOR (v:Vehicle)
    REQUIRE v.vehicle_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT location_id_unique IF NOT EXISTS
    FOR (l:Location)
    REQUIRE l.location_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT organization_id_unique IF NOT EXISTS
    FOR (o:Organization)
    REQUIRE o.organization_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT account_id_unique IF NOT EXISTS
    FOR (a:Account)
    REQUIRE a.account_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT fir_id_unique IF NOT EXISTS
    FOR (f:FIR)
    REQUIRE f.fir_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT crime_id_unique IF NOT EXISTS
    FOR (c:Crime)
    REQUIRE c.crime_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT station_id_unique IF NOT EXISTS
    FOR (s:PoliceStation)
    REQUIRE s.station_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT statute_id_unique IF NOT EXISTS
    FOR (s:Statute)
    REQUIRE s.statute_id IS UNIQUE
    """
]


def create_constraints():

    client = Neo4jClient()

    try:

        client.verify_connection()

        for query in CONSTRAINTS:

            client.execute(query)

        print("✓ All constraints created")

    finally:

        client.close()


if __name__ == "__main__":
    create_constraints()