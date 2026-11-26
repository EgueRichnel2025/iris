import numpy as np
import pytest

from iris.vision.glasses import GlassesStyle, draw_glasses


def face_landmarks():
    points = np.full((478, 3), 0.5, dtype=np.float32)
    points[33] = (0.35, 0.42, 0.0)
    points[133] = (0.45, 0.42, 0.0)
    points[263] = (0.65, 0.42, 0.0)
    points[362] = (0.55, 0.42, 0.0)
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
    with pytest.raises(ValueError, match="363"):
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
