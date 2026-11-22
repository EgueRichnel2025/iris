"""Fast, local image effects applied to OpenCV BGR frames."""

from __future__ import annotations

import cv2
import numpy as np

EFFECTS: tuple[tuple[str, str], ...] = (
    ("original", "Original"),
    ("warm", "Warm glow"),
    ("cool", "Cool tone"),
    ("noir", "Noir"),
    ("vivid", "Vivid"),
    ("soft", "Soft focus"),
)


def apply_effect(frame: np.ndarray, effect: str) -> np.ndarray:
    """Return a processed BGR frame without mutating the camera buffer."""
    if frame is None or frame.size == 0:
        raise ValueError("A non-empty camera frame is required.")

    if effect == "original":
        return frame.copy()

    if effect in {"warm", "cool"}:
        result = frame.astype(np.float32)
        if effect == "warm":
            result *= np.array([0.88, 1.02, 1.14], dtype=np.float32)
        else:
            result *= np.array([1.14, 1.04, 0.90], dtype=np.float32)
        return np.clip(result, 0, 255).astype(np.uint8)

    if effect == "noir":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        contrasted = cv2.convertScaleAbs(gray, alpha=1.15, beta=8)
        return cv2.cvtColor(contrasted, cv2.COLOR_GRAY2BGR)

    if effect == "vivid":
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1].astype(np.float32) * 1.35, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2].astype(np.float32) * 1.05, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    if effect == "soft":
        blurred = cv2.GaussianBlur(frame, (0, 0), sigmaX=2.2)
        return cv2.addWeighted(frame, 1.25, blurred, -0.25, 8)

    raise ValueError(f"Unknown effect: {effect}")
