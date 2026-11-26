import numpy as np
import pytest

from iris.vision.overlay import draw_landmarks


def test_draws_landmark_points_on_a_copy_of_the_frame():
    frame = np.zeros((100, 200, 3), dtype=np.uint8)
    landmarks = np.array([[0.5, 0.5, 0.0], [0.25, 0.25, 0.0]], dtype=np.float32)

    output = draw_landmarks(frame, (landmarks,), radius=2)

    assert output.shape == frame.shape
    assert output.dtype == np.uint8
    assert not np.array_equal(output, frame)
    assert np.count_nonzero(frame) == 0
    assert np.count_nonzero(output) > 0


def test_empty_faces_return_an_unchanged_copy():
    frame = np.full((20, 30, 3), 42, dtype=np.uint8)

    output = draw_landmarks(frame, ())

    np.testing.assert_array_equal(output, frame)
    assert output is not frame


@pytest.mark.parametrize(
    "frame",
    [
        np.zeros((10, 10), dtype=np.uint8),
        np.zeros((10, 10, 4), dtype=np.uint8),
        np.zeros((0, 10, 3), dtype=np.uint8),
        np.zeros((10, 10, 3), dtype=np.float32),
    ],
)
def test_rejects_invalid_frames(frame):
    with pytest.raises(ValueError, match="frame_bgr"):
        draw_landmarks(frame, ())


def test_rejects_non_positive_radius():
    with pytest.raises(ValueError, match="radius"):
        draw_landmarks(np.zeros((10, 10, 3), dtype=np.uint8), (), radius=0)
