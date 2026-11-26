"""Tests for temporal facial-landmark smoothing."""

import numpy as np
import pytest

from iris.vision.smoothing import LandmarkSmoother


def test_first_observation_is_returned_without_smoothing() -> None:
    smoother = LandmarkSmoother(alpha=0.5)
    landmarks = np.array([[0.2, 0.4], [0.8, 0.6]], dtype=np.float32)

    result = smoother.smooth(landmarks)

    np.testing.assert_array_equal(result, landmarks)
    assert result is not landmarks


def test_ema_combines_current_and_previous_landmarks() -> None:
    smoother = LandmarkSmoother(alpha=0.25)
    smoother.smooth(np.array([[0.0, 0.0]], dtype=np.float32))

    result = smoother.smooth(np.array([[1.0, 1.0]], dtype=np.float32))

    np.testing.assert_allclose(result, [[0.25, 0.25]])


def test_alpha_one_tracks_current_frame_exactly() -> None:
    smoother = LandmarkSmoother(alpha=1.0)
    smoother.smooth(np.array([[1.0, 2.0]], dtype=np.float32))

    result = smoother.smooth(np.array([[8.0, 9.0]], dtype=np.float32))

    np.testing.assert_array_equal(result, [[8.0, 9.0]])


def test_alpha_zero_keeps_previous_position() -> None:
    smoother = LandmarkSmoother(alpha=0.0)
    smoother.smooth(np.array([[1.0, 2.0]], dtype=np.float32))

    result = smoother.smooth(np.array([[8.0, 9.0]], dtype=np.float32))

    np.testing.assert_array_equal(result, [[1.0, 2.0]])


def test_shape_change_reinitializes_smoother() -> None:
    smoother = LandmarkSmoother(alpha=0.5)
    smoother.smooth(np.array([[1.0, 2.0]], dtype=np.float32))

    result = smoother.smooth(np.array([[8.0, 9.0], [3.0, 4.0]], dtype=np.float32))

    np.testing.assert_array_equal(result, [[8.0, 9.0], [3.0, 4.0]])


def test_reset_reinitializes_smoother() -> None:
    smoother = LandmarkSmoother(alpha=0.5)
    smoother.smooth(np.array([[0.0, 0.0]], dtype=np.float32))
    smoother.reset()

    result = smoother.smooth(np.array([[1.0, 1.0]], dtype=np.float32))

    np.testing.assert_array_equal(result, [[1.0, 1.0]])


@pytest.mark.parametrize("alpha", [-0.01, 1.01])
def test_alpha_outside_range_is_rejected(alpha: float) -> None:
    with pytest.raises(ValueError, match="alpha"):
        LandmarkSmoother(alpha=alpha)


@pytest.mark.parametrize(
    "landmarks",
    [
        np.array([]),
        np.zeros((2, 4)),
        np.zeros((2, 2, 1)),
        np.array([[np.nan, 0.0]]),
    ],
)
def test_invalid_landmarks_are_rejected(landmarks: np.ndarray) -> None:
    with pytest.raises(ValueError, match="landmarks"):
        LandmarkSmoother().smooth(landmarks)
