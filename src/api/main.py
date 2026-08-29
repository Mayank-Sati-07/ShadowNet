import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

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
from src.api.routes import anomalies
from src.api.routes import transactions

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "The request payload or query parameters are invalid.",
            "details": exc.errors(),
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail if isinstance(exc.detail, str) else "Request failed.",
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected server error occurred. Please try again later.",
        },
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
app.include_router(anomalies.router)
app.include_router(transactions.router)


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


@app.get("/api/health")
def api_health():
    return health()