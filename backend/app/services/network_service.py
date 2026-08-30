from app.core.database import execute_query


def get_network_stats():

    node_query = """
    MATCH (n)
    UNWIND labels(n) AS label
    RETURN label, count(*) AS count
    ORDER BY count DESC
    """

    relationship_query = """
    MATCH ()-[r]->()
    RETURN type(r) AS relationship, count(*) AS count
    ORDER BY count DESC
    """

    nodes = execute_query(node_query)
    relationships = execute_query(relationship_query)

    entities = {
        row["label"]: row["count"]
        for row in nodes
    }

    relation_counts = {
        row["relationship"]: row["count"]
        for row in relationships
    }

    return {
        "total_nodes": sum(entities.values()),
        "total_relationships": sum(
            relation_counts.values()
        ),
        "entities": entities,
        "relationships": relation_counts,
    }


def get_top_persons(
    metric: str = "pagerank",
    limit: int = 10,
):

    allowed_metrics = {
        "degree",
        "degree_centrality",
        "betweenness",
        "pagerank",
    }

    if metric not in allowed_metrics:
        metric = "pagerank"

    query = f"""
    MATCH (p:Person)

    WHERE p.{metric} IS NOT NULL

    RETURN
        p.person_id AS person_id,
        p.degree AS degree,
        p.degree_centrality AS degree_centrality,
        p.betweenness AS betweenness,
        p.pagerank AS pagerank,
        p.community_id AS community_id,
        p.community_size AS community_size

    ORDER BY p.{metric} DESC

    LIMIT $limit
    """

    return execute_query(
        query,
        {"limit": limit},
    )