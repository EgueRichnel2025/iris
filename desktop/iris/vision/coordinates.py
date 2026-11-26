"""Coordinate conversion helpers for facial landmarks."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def normalized_to_pixels(
    landmarks: NDArray[np.floating],
    image_width: int,
    image_height: int,
) -> NDArray[np.float32]:
    """Convert normalized image coordinates to pixel coordinates.

    X and Z are scaled by image width; Y is scaled by image height, following
    MediaPipe's normalized landmark coordinate convention.
    """
    if image_width <= 0 or image_height <= 0:
        raise ValueError("image dimensions must be positive")

    points = np.asarray(landmarks, dtype=np.float32)
    if points.ndim != 2 or points.shape[0] == 0 or points.shape[1] not in (2, 3):
        raise ValueError("landmarks must have shape (N, 2) or (N, 3), with N > 0")
    if not np.isfinite(points).all():
        raise ValueError("landmarks must contain only finite coordinates")

    pixels = points.copy()
    pixels[:, 0] *= image_width
    pixels[:, 1] *= image_height
    if pixels.shape[1] == 3:
        pixels[:, 2] *= image_width
    return pixels
