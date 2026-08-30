from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends

from src.agent.tools import InvestigationTools


router = APIRouter(
    prefix="/api",
    tags=["Search"]
)


class SearchRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000
    )


def get_tools():
    return InvestigationTools()


@router.post("/search")
def search_documents(
    request: SearchRequest,
    tools: InvestigationTools = Depends(get_tools)
):
    result = tools.search_documents(
        request.question
    )

    return result