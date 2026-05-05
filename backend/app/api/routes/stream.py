from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.dependencies import face_detection_service, stream_hub, stream_state_service
from app.db.session import SessionLocal
from app.repositories.roi_repository import ROIRepository
from app.schemas.stream import StreamMessage
from app.services.frame_codec import FrameCodec
from app.services.roi_service import ROIService

router = APIRouter()


@router.websocket("/ws/ingest")
async def ingest_video_feed(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            raw_message = await websocket.receive_json()
            message = StreamMessage.model_validate(raw_message)
            if isinstance(message.frame, str):
                try:
                    frame_rgb = FrameCodec.decode_to_rgb_array(message.frame)
                    message.roi = face_detection_service.detect_single_face_roi(
                        frame_rgb=frame_rgb,
                        frame_id=message.frame_id,
                    )
                    annotated_rgb = FrameCodec.draw_roi_rectangle(frame_rgb, message.roi)
                    message.frame = FrameCodec.encode_rgb_array_to_data_url(annotated_rgb)
                except Exception:
                    # Keep ingest resilient; malformed frames become no-detection ROI.
                    message.roi = face_detection_service.empty_roi(frame_id=message.frame_id)

            payload = stream_state_service.apply_ingest_message(message)

            with SessionLocal() as db_session:
                roi_service = ROIService(ROIRepository(db_session))
                roi_service.save_latest(payload.roi)

            await stream_hub.broadcast(payload.model_dump(mode="json"))
    except WebSocketDisconnect:
        return


@router.websocket("/ws/stream")
async def stream_processed_video(websocket: WebSocket) -> None:
    await stream_hub.connect(websocket)
    try:
        payload = stream_state_service.get_latest_payload()
        await websocket.send_json(payload.model_dump(mode="json"))
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        stream_hub.disconnect(websocket)
