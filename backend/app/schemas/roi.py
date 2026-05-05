from datetime import UTC, datetime

from pydantic import BaseModel, Field


class ROIData(BaseModel):
    frame_id: int = Field(default=0, ge=0)
    x: int = Field(default=0, ge=0)
    y: int = Field(default=0, ge=0)
    width: int = Field(default=0, ge=0)
    height: int = Field(default=0, ge=0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    detected: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
