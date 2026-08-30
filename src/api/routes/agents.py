from fastapi import APIRouter

router = APIRouter(prefix="/api/agents", tags=["Agents"])


@router.get("/status")
def agent_status():
    return {
        "agents": [
            {
                "name": "Graph Agent",
                "status": "online",
                "description": "Path analysis and relationship discovery",
            },
            {
                "name": "FIR/RAG Agent",
                "status": "online",
                "description": "Document retrieval and evidence grounding",
            },
            {
                "name": "Finance Agent",
                "status": "online",
                "description": "Transaction anomaly and laundering assessment",
            },
        ]
    }
