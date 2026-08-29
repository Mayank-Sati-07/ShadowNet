from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from src.agent.tools import InvestigationTools


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


@router.post("/search")
async def search_uploaded_document(
    file: UploadFile = File(...)
):
    """
    Temporary document endpoint.

    M12 initially exposes document ingestion through the API.
    Actual persistent ingestion can be connected to the
    existing FIR → BGE-M3 → Pinecone pipeline.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    content = await file.read()

    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "status": "received"
    }