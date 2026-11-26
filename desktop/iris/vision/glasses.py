"""Face-anchored glasses accessory rendering."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from numpy.typing import NDArray

from iris.vision.coordinates import normalized_to_pixels


@dataclass(frozen=True, slots=True)
class GlassesStyle:
    """Visual parameters for the first IRIS glasses accessory."""

    frame_color: tuple[int, int, int] = (35, 35, 38)
    lens_color: tuple[int, int, int] = (90, 105, 120)
    frame_thickness: int = 3
    lens_opacity: float = 0.32
    width_factor: float = 1.65
    height_factor: float = 0.62


def draw_glasses(
    frame_bgr: NDArray[np.uint8],
    landmarks: NDArray[np.floating],
    *,
    style: GlassesStyle = GlassesStyle(),
) -> NDArray[np.uint8]:
    """Draw glasses anchored to MediaPipe eye landmarks without mutating input."""
    if (
        not isinstance(frame_bgr, np.ndarray)
        or frame_bgr.ndim != 3
        or frame_bgr.shape[2] != 3
        or frame_bgr.size == 0
        or frame_bgr.dtype != np.uint8
    ):
        raise ValueError("frame_bgr must be a non-empty HxWx3 uint8 image")
    points = np.asarray(landmarks, dtype=np.float32)
    if points.ndim != 2 or points.shape[0] < 363 or points.shape[1] not in (2, 3):
        raise ValueError("landmarks must contain at least 363 2D or 3D points")
    if not np.isfinite(points).all():
        raise ValueError("landmarks must contain only finite coordinates")
    if style.frame_thickness < 1:
        raise ValueError("frame_thickness must be at least 1")
    if not 0.0 <= style.lens_opacity <= 1.0:
        raise ValueError("lens_opacity must be between 0 and 1")
    if style.width_factor <= 0 or style.height_factor <= 0:
        raise ValueError("lens dimensions factors must be positive")

    height, width = frame_bgr.shape[:2]
    pixels = normalized_to_pixels(points, width, height)
    # MediaPipe eye corners: 33/133 and 263/362.
    eye_pairs = ((33, 133), (263, 362))
    geometry: list[
        tuple[tuple[int, int], tuple[int, int], tuple[int, int], float, int, int]
    ] = []

    for outer_id, inner_id in eye_pairs:
        outer = pixels[outer_id, :2]
        inner = pixels[inner_id, :2]
        delta = inner - outer
        eye_width = float(np.linalg.norm(delta))
        if eye_width < 2.0:
            raise ValueError("eye landmarks are too close to render glasses")
        center = (outer + inner) / 2.0
        lens_width = max(8, int(round(eye_width * style.width_factor)))
        lens_height = max(6, int(round(lens_width * style.height_factor)))
        angle = float(np.degrees(np.arctan2(delta[1], delta[0])))
        center_px = (int(round(float(center[0]))), int(round(float(center[1]))))
        outer_px = (int(round(float(outer[0]))), int(round(float(outer[1]))))
        inner_px = (int(round(float(inner[0]))), int(round(float(inner[1]))))
        geometry.append((center_px, outer_px, inner_px, angle, lens_width, lens_height))

    output = frame_bgr.copy()
    tinted = output.copy()
    for center, _outer, _inner, angle, lens_width, lens_height in geometry:
        cv2.ellipse(
            tinted, center, (lens_width // 2, lens_height // 2),
            angle, 0, 360, style.lens_color, thickness=-1, lineType=cv2.LINE_AA,
        )
    output = cv2.addWeighted(
        tinted, style.lens_opacity, output, 1.0 - style.lens_opacity, 0
    )

    for center, _outer, _inner, angle, lens_width, lens_height in geometry:
        cv2.ellipse(
            output, center, (lens_width // 2, lens_height // 2),
            angle, 0, 360, style.frame_color,
            thickness=style.frame_thickness, lineType=cv2.LINE_AA,
        )

    left, right = geometry
    cv2.line(
        output, left[2], right[2], style.frame_color,
        thickness=style.frame_thickness, lineType=cv2.LINE_AA,
    )

    # Each temple extends from its outer corner away from the bridge.
    for _center, outer, _inner, _angle, lens_width, _lens_height in geometry:
        outward = np.asarray(outer, dtype=np.float32) - np.asarray(_center, dtype=np.float32)
        norm = float(np.linalg.norm(outward))
        outward /= max(norm, 1.0)
        end = (
            int(round(outer[0] + outward[0] * lens_width * 0.48)),
            int(round(outer[1] + outward[1] * lens_width * 0.48)),
        )
        cv2.line(
            output, outer, end, style.frame_color,
            thickness=style.frame_thickness, lineType=cv2.LINE_AA,
        )
    return output
