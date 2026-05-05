from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.roi_record import ROIRecord
from app.schemas.roi import ROIData


class ROIRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create(self, roi_data: ROIData) -> ROIRecord:
        record = ROIRecord(**roi_data.model_dump())
        self.db_session.add(record)
        self.db_session.commit()
        self.db_session.refresh(record)
        return record

    def get_latest(self) -> ROIRecord | None:
        stmt = select(ROIRecord).order_by(ROIRecord.timestamp.desc(), ROIRecord.id.desc())
        return self.db_session.execute(stmt).scalars().first()
