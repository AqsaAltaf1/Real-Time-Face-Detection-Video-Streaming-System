from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.roi import router as roi_router
from app.api.routes.stream import router as stream_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(stream_router, tags=["stream"])
api_router.include_router(roi_router, prefix="/roi", tags=["roi"])
