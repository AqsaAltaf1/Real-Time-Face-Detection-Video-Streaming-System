import base64
from io import BytesIO

import numpy as np
from PIL import Image, ImageDraw

from app.schemas.roi import ROIData


class FrameCodec:
    """Decode/encode frame payloads and draw ROI rectangles without OpenCV."""

    @staticmethod
    def decode_to_rgb_array(frame_payload: str) -> np.ndarray:
        encoded = frame_payload
        if "," in frame_payload and frame_payload.startswith("data:"):
            _, encoded = frame_payload.split(",", 1)

        raw = base64.b64decode(encoded)
        image = Image.open(BytesIO(raw)).convert("RGB")
        return np.asarray(image)

    @staticmethod
    def draw_roi_rectangle(frame_rgb: np.ndarray, roi: ROIData) -> np.ndarray:
        image = Image.fromarray(frame_rgb)
        if roi.detected and roi.width > 0 and roi.height > 0:
            draw = ImageDraw.Draw(image)
            x1 = roi.x
            y1 = roi.y
            x2 = roi.x + roi.width
            y2 = roi.y + roi.height
            draw.rectangle([(x1, y1), (x2, y2)], outline=(0, 255, 0), width=3)
        return np.asarray(image)

    @staticmethod
    def encode_rgb_array_to_data_url(frame_rgb: np.ndarray) -> str:
        image = Image.fromarray(frame_rgb)
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        return f"data:image/jpeg;base64,{encoded}"
