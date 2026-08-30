from fastapi import APIRouter
from src.api.services.neo4j_service import Neo4jService

router = APIRouter(
    prefix="/api/network",
    tags=["Network"]
)

neo4j = Neo4jService()


@router.get("/stats")
def network_stats():

    query = """
    MATCH (n)
    WITH labels(n)[0] AS label, count(n) AS count
    RETURN label, count
    UNION ALL
    MATCH ()-[r:TRANSFERRED_MONEY]->()
    RETURN 'Transaction' AS label, count(r) AS count
    """

    rows = neo4j.execute(query)

    stats = {
        row["label"]: row["count"]
        for row in rows
        if row.get("label")
    }

    total_nodes = neo4j.execute("MATCH (n) RETURN count(n) AS count")[0]["count"]

    return {
        "total_nodes": total_nodes,
        "entities": stats
    }

@router.get("/relationships")
def relationship_stats():

    query = """
    MATCH ()-[r]->()
    RETURN
        type(r) AS relationship,
        count(r) AS count
    ORDER BY count DESC
    """

    return {
        "relationships": neo4j.execute(query)
    }

@router.get("/top-persons")
def top_persons(
    metric: str = "pagerank",
    limit: int = 20
):

    allowed = {
        "pagerank": "p.pagerank",
        "degree": "p.degree",
        "betweenness": "p.betweenness",
        "degree_centrality": "p.degree_centrality"
    }

    if metric not in allowed:
        return {
            "error": "Invalid metric"
        }

    query = f"""
    MATCH (p:Person)
    
    RETURN
        p.person_id AS person_id,
        p.name AS name,
        coalesce(p.degree, 0) AS degree,
        coalesce(p.degree_centrality, 0.0) AS degree_centrality,
        coalesce(p.betweenness, 0.0) AS betweenness,
        coalesce(p.pagerank, 0.0) AS pagerank,
        p.community_id AS community_id

    ORDER BY coalesce({allowed[metric]}, 0.0) DESC
    LIMIT $limit
    """

    return {
        "metric": metric,
        "persons": neo4j.execute(
            query,
            {"limit": limit}
        )
    }