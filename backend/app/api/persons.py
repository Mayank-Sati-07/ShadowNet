from fastapi import APIRouter, HTTPException

from app.services.person_service import (
    get_person,
    get_connections,
    get_relationship_summary,
)


router = APIRouter()


@router.get("/{person_id}")
def person_details(person_id: str):

    person = get_person(person_id)

    if not person:
        raise HTTPException(
            status_code=404,
            detail="Person not found",
        )

    return person


@router.get("/{person_id}/connections")
def person_connections(person_id: str):

    person = get_person(person_id)

    if not person:
        raise HTTPException(
            status_code=404,
            detail="Person not found",
        )

    connections = get_connections(person_id)

    return {
        "person_id": person_id,
        "count": len(connections),
        "connections": connections,
    }


@router.get("/{person_id}/relationships")
def person_relationships(person_id: str):

    return {
        "person_id": person_id,
        "relationships": get_relationship_summary(
            person_id
        ),
    }