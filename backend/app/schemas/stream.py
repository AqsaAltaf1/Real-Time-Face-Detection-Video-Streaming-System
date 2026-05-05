from pydantic import BaseModel

from app.schemas.roi import ROIData


class StreamMessage(BaseModel):
    frame: str | None = None
    roi: ROIData | None = None


class StreamPayload(BaseModel):
    frame: str | None = None
    roi: ROIData
    frames_received: int
