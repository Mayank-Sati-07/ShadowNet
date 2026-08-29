import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.api.routes import persons
from src.api.routes import network
from src.api.routes import graph
from src.api.routes import intelligence
from src.api.routes import cases
from src.api.routes import agents
from src.api.routes import evidence
from src.api.routes import graph_rag
from src.api.routes import investigation

app = FastAPI(
    title="CNAS API",
    description="Criminal Network Analysis System",
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(persons.router)
app.include_router(network.router)
app.include_router(graph.router)
app.include_router(intelligence.router)
app.include_router(cases.router)
app.include_router(agents.router)
app.include_router(evidence.router)
app.include_router(graph_rag.router)
app.include_router(investigation.router)


@app.get("/")
def root():
    return {
        "name": "CNAS",
        "status": "running",
        "version": settings.app_version,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "cnas-api",
        "version": settings.app_version,
        "components": {
            "neo4j": bool(settings.neo4j_uri),
            "pinecone": bool(settings.pinecone_api_key),
            "google": bool(settings.google_api_key),
            "frontend": bool(settings.allowed_origins),
        },
        "environment": settings.environment,
    }