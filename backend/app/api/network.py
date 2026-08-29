from fastapi import APIRouter, Query

from app.services.network_service import (
    get_network_stats,
    get_top_persons,
)


router = APIRouter()


@router.get("/stats")
def network_stats():

    return get_network_stats()


@router.get("/top-persons")
def top_persons(
    metric: str = Query(
        "pagerank",
        pattern="^(degree|degree_centrality|betweenness|pagerank)$",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
    ),
):

    persons = get_top_persons(
        metric,
        limit,
    )

    return {
        "count": len(persons),
        "metric": metric,
        "persons": persons,
    }