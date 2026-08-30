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
    MATCH ()-[t:TRANSFERRED_MONEY]->()

    WHERE toInteger(t.is_anomaly) > 0 OR t.is_anomaly = true

    RETURN
        t.relationship_id AS transaction_id,
        t.amount AS amount,
        t.timestamp AS timestamp,
        t.confidence AS anomaly_score,
        toBoolean(t.is_anomaly) AS is_anomaly

    ORDER BY t.confidence DESC
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