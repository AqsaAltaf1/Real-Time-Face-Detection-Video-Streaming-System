from fastapi import APIRouter

from app.dependencies import stream_state_service
from app.db.session import SessionLocal
from app.repositories.roi_repository import ROIRepository
from app.schemas.roi import ROIData
from app.services.roi_service import ROIService

router = APIRouter()


@router.get("/latest", response_model=ROIData)
def get_latest_roi() -> ROIData:
    with SessionLocal() as db_session:
        roi_service = ROIService(ROIRepository(db_session))
        db_roi = roi_service.get_latest()

    if db_roi is not None:
        return db_roi

    return stream_state_service.get_latest_roi()
