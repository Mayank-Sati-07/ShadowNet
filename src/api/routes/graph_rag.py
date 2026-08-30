from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from src.api.dependencies import get_investigation_agent

router = APIRouter(prefix="/api/graph-rag", tags=["GraphRAG"])


class GraphRAGRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)


@router.get("/status")
def graph_rag_status():
    return {
        "status": "online",
        "components": [
            "neo4j_graph",
            "vector_retrieval",
            "graph_agent",
            "evidence_aggregation",
            "final_answer",
        ],
        "description": "GraphRAG pipeline for connected-entity investigation and evidence grounding.",
    }


@router.post("/investigate")
def investigate(
    request: GraphRAGRequest,
    agent=Depends(get_investigation_agent),
):
    try:
        result = agent.ask(request.question)
        return {
            "question": request.question,
            "status": "success",
            "answer": result.get("final_answer", ""),
            "graph_evidence": result.get("graph_evidence", []),
            "document_evidence": result.get("document_evidence", []),
            "investigation_evidence": result.get("investigation_evidence", {}),
        }
    except Exception as exc:  # pragma: no cover - defensive route guard
        return {
            "question": request.question,
            "status": "error",
            "answer": f"GraphRAG investigation failed: {exc}",
            "graph_evidence": [],
            "document_evidence": [],
            "investigation_evidence": {},
        }
