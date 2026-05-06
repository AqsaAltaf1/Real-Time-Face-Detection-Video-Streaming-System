from datetime import UTC, datetime

from app.schemas.roi import ROIData
from app.schemas.stream import StreamMessage, StreamPayload


class StreamStateService:
    """In-memory state service for chunk 1 contracts."""

    def __init__(self) -> None:
        self.latest_frame: str | None = None
        self.latest_roi: ROIData = ROIData()
        self.frames_received: int = 0

    def apply_ingest_message(self, message: StreamMessage) -> StreamPayload:
        if isinstance(message.frame, str):
            self.latest_frame = message.frame

        if message.roi is not None:
            self.latest_roi = message.roi
        else:
            self.latest_roi.timestamp = datetime.now(UTC)

        self.frames_received += 1
        return self.get_latest_payload()

    def get_latest_payload(self) -> StreamPayload:
        return StreamPayload(
            frame=self.latest_frame,
            roi=self.latest_roi,
            frames_received=self.frames_received,
        )

    def get_latest_roi(self) -> ROIData:
        return self.latest_roi
