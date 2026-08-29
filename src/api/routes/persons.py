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
        coalesce(p.name, p.person_id) AS name,
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
        coalesce(p.name, p.person_id) AS name,
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


@router.get("/{person_id}/network")
def get_person_network(person_id: str):
    person = get_person(person_id)

    query = """
    MATCH (p:Person {person_id: $person_id})-[r]-(other)
    RETURN
        coalesce(
            other.person_id,
            other.fir_id,
            other.account_id,
            other.phone_id,
            other.vehicle_id,
            other.location_id,
            other.organization_id,
            labels(other)[0]
        ) AS id,
        coalesce(
            other.name,
            other.person_id,
            other.fir_id,
            other.account_id,
            other.phone_id,
            other.vehicle_id,
            other.location_id,
            other.organization_id,
            labels(other)[0]
        ) AS name,
        labels(other) AS type,
        type(r) AS relationship
    ORDER BY type(r), id
    LIMIT 200
    """

    connections = neo4j.execute(query, {"person_id": person_id})

    return {
        "person_id": person_id,
        "name": person.get("name") or person_id,
        "degree": person.get("degree"),
        "degree_centrality": person.get("degree_centrality"),
        "betweenness": person.get("betweenness"),
        "pagerank": person.get("pagerank"),
        "community": person.get("community_id"),
        "community_size": person.get("community_size"),
        "connections": connections,
    }


@router.get("/{person_id}/anomalies")
def get_person_anomalies(person_id: str):
    query = """
    MATCH (p:Person {person_id: $person_id})-[r]-(t:Transaction)
    WHERE coalesce(r.is_anomaly, t.is_anomaly, false) = true
       OR coalesce(r.anomaly_score, t.anomaly_score, 0) > 0
    RETURN
        coalesce(t.id, r.id) AS transaction_id,
        t.amount AS amount,
        t.timestamp AS timestamp,
        coalesce(r.anomaly_score, t.anomaly_score, 0) AS anomaly_score,
        coalesce(r.is_anomaly, t.is_anomaly, false) AS is_anomaly
    ORDER BY anomaly_score DESC
    LIMIT 50
    """

    rows = neo4j.execute(query, {"person_id": person_id})
    return {
        "person_id": person_id,
        "count": len(rows),
        "anomalies": rows,
    }


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