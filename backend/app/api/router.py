from fastapi import APIRouter

from app.api.network import router as network_router
from app.api.persons import router as persons_router
from app.api.transactions import router as transactions_router
from app.api.anomalies import router as anomalies_router
from app.api.risk import router as risk_router
from app.api.communities import router as communities_router
from app.api.links import router as links_router
from app.api.timeline import router as timeline_router
from app.api.locations import router as locations_router
from app.api.cases import router as cases_router


api_router = APIRouter()


api_router.include_router(
    network_router,
    prefix="/network",
    tags=["Network"],
)

api_router.include_router(
    persons_router,
    prefix="/persons",
    tags=["Persons"],
)

api_router.include_router(
    transactions_router,
    prefix="/transactions",
    tags=["Transactions"],
)

api_router.include_router(
    anomalies_router,
    prefix="/anomalies",
    tags=["Anomalies"],
)

api_router.include_router(
    risk_router,
    prefix="/risk",
    tags=["Risk"],
)

api_router.include_router(
    communities_router,
    prefix="/communities",
    tags=["Communities"],
)

api_router.include_router(
    links_router,
    prefix="/links",
    tags=["Link Prediction"],
)

api_router.include_router(
    timeline_router,
    prefix="/timeline",
    tags=["Timeline"],
)

api_router.include_router(
    locations_router,
    prefix="/locations",
    tags=["Locations"],
)

api_router.include_router(
    cases_router,
    prefix="/cases",
    tags=["Cases"],
)