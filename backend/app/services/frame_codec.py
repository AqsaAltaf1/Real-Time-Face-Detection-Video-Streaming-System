import base64
from io import BytesIO

import numpy as np
from PIL import Image


class FrameCodec:
    """Decode base64/data-url frame strings into RGB numpy arrays."""

    @staticmethod
    def decode_to_rgb_array(frame_payload: str) -> np.ndarray:
        encoded = frame_payload
        if "," in frame_payload and frame_payload.startswith("data:"):
            _, encoded = frame_payload.split(",", 1)

        raw = base64.b64decode(encoded)
        image = Image.open(BytesIO(raw)).convert("RGB")
        return np.asarray(image)
