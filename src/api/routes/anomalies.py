from fastapi import APIRouter, Depends, Query

from src.graph.investigation_service import GraphInvestigationService
from src.api.dependencies import get_graph_service


router = APIRouter(
    prefix="/api/anomalies",
    tags=["Anomalies"]
)


@router.get("")
def list_anomalies(
    limit: int = Query(100, ge=1, le=1000),
    graph: GraphInvestigationService = Depends(get_graph_service)
):
    query = """
    MATCH (t:Transaction)

    WHERE t.is_anomaly = true

    RETURN
        t.id AS transaction_id,
        t.amount AS amount,
        t.timestamp AS timestamp,
        t.anomaly_score AS anomaly_score,
        t.is_anomaly AS is_anomaly

    ORDER BY t.anomaly_score DESC
    LIMIT $limit
    """

    records = graph.client.execute_read(
        query,
        {"limit": limit}
    )

    return {
        "count": len(records),
        "anomalies": [
            dict(record)
            for record in records
        ]
    }