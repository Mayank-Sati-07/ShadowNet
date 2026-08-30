from fastapi import APIRouter

router = APIRouter(prefix="/api/evidence", tags=["Evidence"])


@router.get("/summary")
def evidence_summary():
    return {
        "total_documents": 184,
        "total_sources": 12,
        "grounded_chains": 39,
        "confidence_average": 0.87,
    }
