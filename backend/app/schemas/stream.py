from pydantic import BaseModel, Field

from app.schemas.roi import ROIData


class StreamMessage(BaseModel):
    frame_id: int = Field(default=0, ge=0)
    frame: str | None = None
    roi: ROIData | None = None


class StreamPayload(BaseModel):
    frame: str | None = None
    roi: ROIData
    frames_received: int
