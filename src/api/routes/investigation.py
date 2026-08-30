from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends

from src.agent.graph import ShadowNetInvestigationAgent
from src.api.dependencies import get_investigation_agent


router = APIRouter(
    prefix="/api",
    tags=["Investigation"]
)


class InvestigationRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000
    )


@router.post("/investigate")
def investigate(
    request: InvestigationRequest,
    agent: ShadowNetInvestigationAgent = Depends(
        get_investigation_agent
    )
):
    """
    Run the ShadowNet LangGraph investigation agent.
    """

    result = agent.ask(
        request.question
    )

    return {
        "question": request.question,
        "answer": result.get(
            "final_answer",
            ""
        ),
        "graph_evidence": result.get(
            "graph_evidence",
            []
        ),
        "document_evidence": result.get(
            "document_evidence",
            []
        ),
        "investigation_evidence": result.get(
            "investigation_evidence",
            {}
        )
    }