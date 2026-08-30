from app.core.database import execute_query


def get_person(person_id: str):

    query = """
    MATCH (p:Person)
    WHERE p.person_id = $person_id

    RETURN
        p.person_id AS person_id,
        p.source AS source,
        p.source_role AS source_role,
        p.confidence AS confidence,
        p.degree AS degree,
        p.degree_centrality AS degree_centrality,
        p.betweenness AS betweenness,
        p.pagerank AS pagerank,
        p.community_id AS community_id,
        p.community_size AS community_size
    """

    results = execute_query(
        query,
        {"person_id": person_id},
    )

    return results[0] if results else None


def get_connections(person_id: str):

    query = """
    MATCH (p:Person)-[r]-(other)

    WHERE p.person_id = $person_id

    RETURN
        p.person_id AS source,
        type(r) AS relationship,
        labels(other) AS target_type,
        coalesce(
            other.person_id,
            other.account_id,
            other.phone_id,
            other.transaction_id,
            other.fir_id,
            other.location_id,
            other.vehicle_id
        ) AS target

    LIMIT 500
    """

    return execute_query(
        query,
        {"person_id": person_id},
    )


def get_relationship_summary(person_id: str):

    query = """
    MATCH (p:Person)-[r]-(other)

    WHERE p.person_id = $person_id

    RETURN
        type(r) AS relationship,
        count(*) AS count

    ORDER BY count DESC
    """

    return execute_query(
        query,
        {"person_id": person_id},
    )