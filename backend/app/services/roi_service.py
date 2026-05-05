from app.models.roi_record import ROIRecord
from app.repositories.roi_repository import ROIRepository
from app.schemas.roi import ROIData


class ROIService:
    def __init__(self, roi_repository: ROIRepository) -> None:
        self.roi_repository = roi_repository

    def save_latest(self, roi_data: ROIData) -> ROIRecord:
        return self.roi_repository.create(roi_data)

    def get_latest(self) -> ROIData | None:
        latest = self.roi_repository.get_latest()
        if latest is None:
            return None
        return ROIData.model_validate(latest, from_attributes=True)
