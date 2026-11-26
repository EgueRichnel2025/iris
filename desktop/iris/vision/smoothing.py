"""Temporal smoothing utilities for facial landmark coordinates."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


class LandmarkSmoother:
    """Smooth landmark coordinates with an exponential moving average.

    The alpha parameter controls how strongly the newest frame influences
    the result: values near 1.0 are responsive, while values near 0.0 are
    smoother but introduce more latency. The first observation is unchanged.
    """

    def __init__(self, alpha: float = 0.65) -> None:
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha must be between 0.0 and 1.0")
        self.alpha = float(alpha)
        self._previous: NDArray[np.float32] | None = None

    def smooth(self, landmarks: NDArray[np.floating]) -> NDArray[np.float32]:
        """Return smoothed landmarks shaped (point_count, 2 or 3)."""
        points = np.asarray(landmarks, dtype=np.float32)
        if points.ndim != 2 or points.shape[0] == 0 or points.shape[1] not in (2, 3):
            raise ValueError("landmarks must have shape (N, 2) or (N, 3), with N > 0")
        if not np.isfinite(points).all():
            raise ValueError("landmarks must contain only finite coordinates")

        if self._previous is None or self._previous.shape != points.shape:
            result = points.copy()
        else:
            result = self.alpha * points + (1.0 - self.alpha) * self._previous

        self._previous = result.copy()
        return result

    def reset(self) -> None:
        """Discard the previous frame, for example after losing the face."""
        self._previous = None
