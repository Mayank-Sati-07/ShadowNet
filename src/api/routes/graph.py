from fastapi import APIRouter
from src.api.services.neo4j_service import Neo4jService

router = APIRouter(
    prefix="/api/graph",
    tags=["Graph"]
)

neo4j = Neo4jService()


@router.get("/path")
def shortest_path(
    source: str,
    target: str
):

    query = """
    MATCH
        (a:Person {person_id: $source}),
        (b:Person {person_id: $target})

    MATCH path = shortestPath(
        (a)-[*..6]-(b)
    )

    RETURN
        [node IN nodes(path) |
            coalesce(
                node.person_id,
                node.fir_id,
                node.account_id,
                node.phone_id
            )
        ] AS nodes,

        [rel IN relationships(path) |
            type(rel)
        ] AS relationships,

        length(path) AS length
    LIMIT 1
    """

    result = neo4j.execute(
        query,
        {
            "source": source,
            "target": target
        }
    )

    return {
        "source": source,
        "target": target,
        "path": result[0] if result else None
    }