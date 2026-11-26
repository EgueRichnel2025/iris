"""Face-anchored glasses accessory rendering."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from numpy.typing import NDArray

from iris.vision.coordinates import normalized_to_pixels


# MediaPipe Face Mesh eye corners and upper/lower eyelid contours.
_EYE_LAYOUTS = (
    (33, 133, (160, 158, 157), (144, 145, 153)),
    (263, 362, (387, 385, 384), (373, 374, 380)),
)


@dataclass(frozen=True, slots=True)
class GlassesStyle:
    """Visual and geometric parameters for the IRIS glasses accessory."""

    frame_color: tuple[int, int, int] = (35, 35, 38)
    lens_color: tuple[int, int, int] = (90, 105, 120)
    frame_thickness: int = 3
    lens_opacity: float = 0.28
    width_factor: float = 1.55
    height_factor: float = 2.1
    minimum_height_ratio: float = 0.34


@dataclass(frozen=True, slots=True)
class LensGeometry:
    """Pixel geometry for one lens, derived from one eye's landmarks."""

    center: tuple[int, int]
    outer_edge: tuple[int, int]
    inner_edge: tuple[int, int]
    angle_degrees: float
    width: int
    height: int
    outward: tuple[float, float]
    contour: tuple[tuple[int, int], ...]


def _validate_style(style: GlassesStyle) -> None:
    for name, color in (
        ("frame_color", style.frame_color),
        ("lens_color", style.lens_color),
    ):
        if (
            not isinstance(color, tuple)
            or len(color) != 3
            or any(not isinstance(channel, int) or not 0 <= channel <= 255 for channel in color)
        ):
            raise ValueError(f"{name} must be a BGR tuple with channels from 0 to 255")
    if style.frame_thickness < 1:
        raise ValueError("frame_thickness must be at least 1")
    if not 0.0 <= style.lens_opacity <= 1.0:
        raise ValueError("lens_opacity must be between 0 and 1")
    if style.width_factor <= 0 or style.height_factor <= 0:
        raise ValueError("lens dimension factors must be positive")
    if not 0.0 < style.minimum_height_ratio <= 1.0:
        raise ValueError("minimum_height_ratio must be in (0, 1]")


def estimate_glasses_geometry(
    landmarks: NDArray[np.floating],
    image_width: int,
    image_height: int,
    *,
    style: GlassesStyle = GlassesStyle(),
) -> tuple[LensGeometry, LensGeometry]:
    """Estimate two independently sized and rotated lenses from eye contours.

    The eye-corner distance controls lens width. Upper/lower eyelid landmarks
    control lens height. Because each eye is measured independently, its
    on-screen width naturally contracts as that side of the face turns away.
    """
    _validate_style(style)
    points = np.asarray(landmarks, dtype=np.float32)
    if points.ndim != 2 or points.shape[0] < 388 or points.shape[1] not in (2, 3):
        raise ValueError("landmarks must contain at least 388 2D or 3D points")
    if not np.isfinite(points).all():
        raise ValueError("landmarks must contain only finite coordinates")
    pixels = normalized_to_pixels(points, image_width, image_height)

    result: list[LensGeometry] = []
    for outer_id, inner_id, upper_ids, lower_ids in _EYE_LAYOUTS:
        outer = pixels[outer_id, :2]
        inner = pixels[inner_id, :2]
        delta = inner - outer
        eye_width = float(np.linalg.norm(delta))
        if eye_width < 2.0:
            raise ValueError("eye landmarks are too close to render glasses")

        horizontal = delta / eye_width
        vertical = np.array((-horizontal[1], horizontal[0]), dtype=np.float32)
        upper = pixels[list(upper_ids), :2].mean(axis=0)
        lower = pixels[list(lower_ids), :2].mean(axis=0)
        eye_opening = abs(float(np.dot(upper - lower, vertical)))
        corner_center = (outer + inner) / 2.0
        lid_center = (upper + lower) / 2.0
        center = (corner_center + lid_center) / 2.0

        lens_width = max(8, int(round(eye_width * style.width_factor)))
        natural_height = eye_opening * style.height_factor
        minimum_height = lens_width * style.minimum_height_ratio
        lens_height = max(6, int(round(max(natural_height, minimum_height))))
        # A malformed or occluded landmark set must not create an oversized lens.
        lens_height = min(lens_height, int(round(lens_width * 0.78)))

        outer_edge = center - horizontal * (lens_width / 2.0)
        inner_edge = center + horizontal * (lens_width / 2.0)
        outward = -horizontal
        to_pixel = lambda value: (int(round(float(value[0]))), int(round(float(value[1]))))

        # Preserve the eye's actual contour, then expand it around its center.
        # This produces a softly polygonal lens instead of a generic ellipse.
        eye_contour = np.vstack((outer, upper, inner, lower[::-1]))
        horizontal_scale = lens_width / eye_width
        vertical_scale = lens_height / max(eye_opening, 1.0)
        contour_points = []
        for point in eye_contour:
            relative = point - center
            along_eye = float(np.dot(relative, horizontal)) * horizontal_scale
            across_eye = float(np.dot(relative, vertical)) * vertical_scale
            expanded = center + horizontal * along_eye + vertical * across_eye
            contour_points.append(to_pixel(expanded))

        result.append(
            LensGeometry(
                center=to_pixel(center),
                outer_edge=to_pixel(outer_edge),
                inner_edge=to_pixel(inner_edge),
                angle_degrees=float(np.degrees(np.arctan2(horizontal[1], horizontal[0]))),
                width=lens_width,
                height=lens_height,
                outward=(float(outward[0]), float(outward[1])),
                contour=tuple(contour_points),
            )
        )

    return result[0], result[1]


def draw_glasses(
    frame_bgr: NDArray[np.uint8],
    landmarks: NDArray[np.floating],
    *,
    style: GlassesStyle = GlassesStyle(),
) -> NDArray[np.uint8]:
    """Draw perspective-adaptive glasses without mutating the camera frame."""
    if (
        not isinstance(frame_bgr, np.ndarray)
        or frame_bgr.ndim != 3
        or frame_bgr.shape[2] != 3
        or frame_bgr.size == 0
        or frame_bgr.dtype != np.uint8
    ):
        raise ValueError("frame_bgr must be a non-empty HxWx3 uint8 image")

    height, width = frame_bgr.shape[:2]
    left, right = estimate_glasses_geometry(
        landmarks, width, height, style=style
    )
    lenses = (left, right)

    # Fill translucent lenses using the expanded eye contours.
    tinted = frame_bgr.copy()
    polygons = [np.asarray(lens.contour, dtype=np.int32) for lens in lenses]
    for polygon in polygons:
        cv2.fillPoly(tinted, [polygon], style.lens_color, lineType=cv2.LINE_AA)
    output = cv2.addWeighted(
        tinted, style.lens_opacity, frame_bgr, 1.0 - style.lens_opacity, 0
    )

    # Draw a continuous frame around each lens contour.
    for polygon in polygons:
        cv2.polylines(
            output, [polygon], isClosed=True, color=style.frame_color,
            thickness=style.frame_thickness, lineType=cv2.LINE_AA,
        )

    # The bridge joins the two inner lens edges, not the eye corners.
    cv2.line(
        output,
        left.inner_edge,
        right.inner_edge,
        style.frame_color,
        thickness=style.frame_thickness,
        lineType=cv2.LINE_AA,
    )

    for lens in lenses:
        end = (
            int(round(lens.outer_edge[0] + lens.outward[0] * lens.width * 0.42)),
            int(round(lens.outer_edge[1] + lens.outward[1] * lens.width * 0.42)),
        )
        cv2.line(
            output,
            lens.outer_edge,
            end,
            style.frame_color,
            thickness=style.frame_thickness,
            lineType=cv2.LINE_AA,
        )

    return output
