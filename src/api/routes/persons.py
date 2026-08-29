from fastapi import APIRouter, HTTPException
from src.api.services.neo4j_service import Neo4jService

router = APIRouter(
    prefix="/api/persons",
    tags=["Persons"]
)

neo4j = Neo4jService()


@router.get("")
def get_persons(limit: int = 50):

    query = """
    MATCH (p:Person)
    RETURN
        p.person_id AS person_id,
        p.name AS name,
        p.source AS source,
        p.source_role AS source_role,
        p.confidence AS confidence,
        p.degree AS degree,
        p.degree_centrality AS degree_centrality,
        p.betweenness AS betweenness,
        p.pagerank AS pagerank,
        p.community_id AS community_id,
        p.community_size AS community_size
    LIMIT $limit
    """

    return {
        "count": limit,
        "persons": neo4j.execute(
            query,
            {"limit": limit}
        )
    }


@router.get("/{person_id}")
def get_person(person_id: str):

    query = """
    MATCH (p:Person {person_id: $person_id})
    RETURN
        p.person_id AS person_id,
        p.name AS name,
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

    result = neo4j.execute(
        query,
        {"person_id": person_id}
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    return result[0]

@router.get("/{person_id}/connections")
def get_connections(person_id: str):

    query = """
    MATCH (p:Person {person_id: $person_id})-[r]-(other)
    RETURN
        p.person_id AS source,
        type(r) AS relationship,
        labels(other) AS target_type,
        coalesce(
            other.person_id,
            other.fir_id,
            other.account_id,
            other.phone_id,
            other.vehicle_id,
            other.location_id,
            other.organization_id
        ) AS target
    LIMIT 500
    """

    return {
        "person_id": person_id,
        "connections": neo4j.execute(
            query,
            {"person_id": person_id}
        )
    }