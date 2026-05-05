from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ROIRecord(Base):
    __tablename__ = "roi_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    frame_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    x: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    y: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    width: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    height: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    detected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
