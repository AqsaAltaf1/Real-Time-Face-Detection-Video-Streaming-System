from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.dependencies import stream_hub, stream_state_service
from app.schemas.stream import StreamMessage

router = APIRouter()


@router.websocket("/ws/ingest")
async def ingest_video_feed(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            raw_message = await websocket.receive_json()
            message = StreamMessage.model_validate(raw_message)
            payload = stream_state_service.apply_ingest_message(message)
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
