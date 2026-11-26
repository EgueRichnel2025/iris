"""Drawing utilities for facial landmarks."""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray

from iris.vision.coordinates import normalized_to_pixels


def draw_landmarks(
    frame_bgr: NDArray[np.uint8],
    faces: tuple[NDArray[np.float32], ...],
    *,
    color: tuple[int, int, int] = (80, 230, 120),
    radius: int = 1,
) -> NDArray[np.uint8]:
    """Return a copy of a BGR frame with detected facial landmarks drawn."""
    if (
        not isinstance(frame_bgr, np.ndarray)
        or frame_bgr.ndim != 3
        or frame_bgr.shape[2] != 3
        or frame_bgr.size == 0
        or frame_bgr.dtype != np.uint8
    ):
        raise ValueError("frame_bgr must be a non-empty HxWx3 uint8 image")
    if radius < 1:
        raise ValueError("radius must be at least 1")

    output = frame_bgr.copy()
    height, width = output.shape[:2]
    for face in faces:
        points = normalized_to_pixels(face, width, height)
        for x, y in points[:, :2]:
            center = (int(round(float(x))), int(round(float(y))))
            cv2.circle(output, center, radius, color, thickness=-1, lineType=cv2.LINE_AA)
    return output
