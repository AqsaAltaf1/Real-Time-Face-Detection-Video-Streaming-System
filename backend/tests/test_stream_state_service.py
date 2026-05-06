from app.schemas.roi import ROIData
from app.schemas.stream import StreamMessage
from app.services.stream_state import StreamStateService


def test_apply_ingest_message_updates_frame_and_roi() -> None:
    service = StreamStateService()
    roi = ROIData(
        frame_id=11,
        x=10,
        y=20,
        width=100,
        height=80,
        confidence=0.9,
        detected=True,
    )
    message = StreamMessage(frame_id=11, frame="data:image/jpeg;base64,abc", roi=roi)

    payload = service.apply_ingest_message(message)

    assert payload.frame == "data:image/jpeg;base64,abc"
    assert payload.frames_received == 1
    assert payload.roi.frame_id == 11
    assert payload.roi.detected is True


def test_apply_ingest_message_without_roi_keeps_valid_default() -> None:
    service = StreamStateService()
    message = StreamMessage(frame_id=5, frame="data:image/jpeg;base64,xyz", roi=None)

    payload = service.apply_ingest_message(message)

    assert payload.frames_received == 1
    assert payload.roi.frame_id >= 0
    assert payload.roi.width >= 0
    assert payload.roi.height >= 0
