import numpy as np
import pytest

from iris.vision.glasses import (
    GlassesStyle,
    draw_glasses,
    estimate_glasses_geometry,
)


LEFT_EYE_IDS = (33, 160, 158, 157, 133, 153, 145, 144)
RIGHT_EYE_IDS = (263, 387, 385, 384, 362, 380, 374, 373)


def face_landmarks():
    points = np.full((478, 3), 0.5, dtype=np.float32)
    # Image-left eye: outer corner -> upper lid -> inner corner -> lower lid.
    points[33] = (0.35, 0.42, 0.0)
    points[160] = (0.37, 0.405, 0.0)
    points[158] = (0.40, 0.400, 0.0)
    points[157] = (0.43, 0.405, 0.0)
    points[133] = (0.45, 0.42, 0.0)
    points[153] = (0.43, 0.435, 0.0)
    points[145] = (0.40, 0.440, 0.0)
    points[144] = (0.37, 0.435, 0.0)

    # Image-right eye, ordered in the same outer-to-inner direction.
    points[263] = (0.65, 0.42, 0.0)
    points[387] = (0.63, 0.405, 0.0)
    points[385] = (0.60, 0.400, 0.0)
    points[384] = (0.57, 0.405, 0.0)
    points[362] = (0.55, 0.42, 0.0)
    points[380] = (0.57, 0.435, 0.0)
    points[374] = (0.60, 0.440, 0.0)
    points[373] = (0.63, 0.435, 0.0)
    return points


def test_draw_glasses_renders_two_lenses_and_frame_on_a_copy():
    frame = np.full((240, 320, 3), 180, dtype=np.uint8)
    original = frame.copy()

    output = draw_glasses(frame, face_landmarks())

    assert output.shape == frame.shape
    assert output.dtype == np.uint8
    assert not np.array_equal(output, original)
    np.testing.assert_array_equal(frame, original)


def test_glasses_support_two_dimensional_landmarks():
    frame = np.zeros((240, 320, 3), dtype=np.uint8)

    output = draw_glasses(frame, face_landmarks()[:, :2])

    assert np.count_nonzero(output) > 0


def test_glasses_style_controls_lens_opacity():
    frame = np.full((240, 320, 3), 180, dtype=np.uint8)
    transparent = draw_glasses(
        frame, face_landmarks(), style=GlassesStyle(lens_opacity=0.0)
    )
    tinted = draw_glasses(
        frame, face_landmarks(), style=GlassesStyle(lens_opacity=1.0)
    )

    assert not np.array_equal(transparent, tinted)


def test_geometry_uses_independent_eye_measurements_for_perspective():
    points = face_landmarks()
    # Foreshorten the image-right eye around its own center to model a head yaw.
    center_x = 0.60
    points[list(RIGHT_EYE_IDS), 0] = (
        center_x + (points[list(RIGHT_EYE_IDS), 0] - center_x) * 0.55
    )

    left, right = estimate_glasses_geometry(points, 640, 480)

    assert right.width < left.width * 0.7
    assert left.width > 0 and right.width > 0


def test_geometry_rotation_follows_eye_line():
    points = face_landmarks()
    ids = list(RIGHT_EYE_IDS)
    center = points[ids, :2].mean(axis=0)
    angle = np.radians(24.0)
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    points[ids, :2] = (points[ids, :2] - center) @ rotation.T + center

    _left, right = estimate_glasses_geometry(points, 640, 480)

    assert abs(right.angle_degrees - 180.0) > 10.0


def test_geometry_uses_eyelid_opening_to_size_lens_height():
    points = face_landmarks()
    baseline = estimate_glasses_geometry(points, 640, 480)[0]
    points[[160, 158, 157], 1] -= 0.012
    points[[144, 145, 153], 1] += 0.012

    wider_opening = estimate_glasses_geometry(points, 640, 480)[0]

    assert wider_opening.height > baseline.height


@pytest.mark.parametrize(
    "frame",
    [
        np.zeros((20, 20), dtype=np.uint8),
        np.zeros((20, 20, 4), dtype=np.uint8),
        np.zeros((0, 20, 3), dtype=np.uint8),
        np.zeros((20, 20, 3), dtype=np.float32),
    ],
)
def test_rejects_invalid_frames(frame):
    with pytest.raises(ValueError, match="frame_bgr"):
        draw_glasses(frame, face_landmarks())


def test_rejects_insufficient_landmarks():
    with pytest.raises(ValueError, match="388"):
        draw_glasses(np.zeros((240, 320, 3), dtype=np.uint8), np.zeros((100, 3)))


def test_rejects_collapsed_eye_landmarks():
    points = face_landmarks()
    points[133] = points[33]

    with pytest.raises(ValueError, match="too close"):
        draw_glasses(np.zeros((240, 320, 3), dtype=np.uint8), points)


def test_rejects_invalid_style():
    with pytest.raises(ValueError, match="lens_opacity"):
        draw_glasses(
            np.zeros((240, 320, 3), dtype=np.uint8),
            face_landmarks(),
            style=GlassesStyle(lens_opacity=1.5),
        )


def test_rejects_invalid_landmark_values():
    points = face_landmarks()
    points[33, 0] = np.nan

    with pytest.raises(ValueError, match="finite"):
        estimate_glasses_geometry(points, 640, 480)
