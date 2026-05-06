from datetime import UTC, datetime

import mediapipe as mp
import numpy as np

from app.schemas.roi import ROIData


class FaceDetectionService:
    """Non-OpenCV face detection using MediaPipe."""

    def __init__(self, min_detection_confidence: float = 0.5) -> None:
        self._detector = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=min_detection_confidence,
        )

    def detect_single_face_roi(self, frame_rgb: np.ndarray, frame_id: int) -> ROIData:
        height, width, _ = frame_rgb.shape
        result = self._detector.process(frame_rgb)

        if not result.detections:
            return self.empty_roi(frame_id=frame_id)

        detection = result.detections[0]
        bbox = detection.location_data.relative_bounding_box

        x_min = max(0, int(bbox.xmin * width))
        y_min = max(0, int(bbox.ymin * height))
        x_max = min(width, int((bbox.xmin + bbox.width) * width))
        y_max = min(height, int((bbox.ymin + bbox.height) * height))

        confidence = float(detection.score[0]) if detection.score else 0.0

        return ROIData(
            frame_id=frame_id,
            x=x_min,
            y=y_min,
            width=max(0, x_max - x_min),
            height=max(0, y_max - y_min),
            confidence=max(0.0, min(1.0, confidence)),
            detected=True,
            timestamp=datetime.now(UTC),
        )

    @staticmethod
    def empty_roi(frame_id: int) -> ROIData:
        return ROIData(
            frame_id=frame_id,
            x=0,
            y=0,
            width=0,
            height=0,
            confidence=0.0,
            detected=False,
            timestamp=datetime.now(UTC),
        )
