"""Fast, local image effects applied to OpenCV BGR frames."""

from __future__ import annotations

import cv2
import numpy as np

EFFECTS: tuple[tuple[str, str], ...] = (
    ("original", "Original"),
    ("warm", "Lueur chaude"),
    ("cool", "Teinte froide"),
    ("noir", "Noir"),
    ("vivid", "Éclatant"),
    ("soft", "Flou doux"),
)


def enhance_camera_lighting(frame: np.ndarray) -> np.ndarray:
    """Lift dark camera shadows while preserving bright areas and color."""
    if frame is None or frame.size == 0:
        raise ValueError("A non-empty camera frame is required.")
    if frame.ndim != 3 or frame.shape[2] != 3 or frame.dtype != np.uint8:
        raise ValueError("frame must be a uint8 BGR image")

    # CLAHE acts on luminance only: it opens underexposed shadows without
    # globally raising the already-bright window behind the subject.
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    luminance, a_channel, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(luminance)
    merged = cv2.merge((enhanced, a_channel, b_channel))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


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
