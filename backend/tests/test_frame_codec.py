import base64
from io import BytesIO

import numpy as np
from PIL import Image

from app.schemas.roi import ROIData
from app.services.frame_codec import FrameCodec


def _sample_data_url() -> str:
    array = np.zeros((16, 16, 3), dtype=np.uint8)
    array[:, :] = [255, 0, 0]
    image = Image.fromarray(array)
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def test_decode_and_encode_roundtrip() -> None:
    payload = _sample_data_url()
    frame_rgb = FrameCodec.decode_to_rgb_array(payload)
    assert frame_rgb.shape[0] == 16
    assert frame_rgb.shape[1] == 16

    output_payload = FrameCodec.encode_rgb_array_to_data_url(frame_rgb)
    assert output_payload.startswith("data:image/jpeg;base64,")


def test_draw_roi_rectangle() -> None:
    payload = _sample_data_url()
    frame_rgb = FrameCodec.decode_to_rgb_array(payload)
    roi = ROIData(frame_id=1, x=2, y=2, width=8, height=8, confidence=0.8, detected=True)

    annotated = FrameCodec.draw_roi_rectangle(frame_rgb, roi)

    assert annotated.shape == frame_rgb.shape
