import numpy as np
import pytest

from iris.vision.coordinates import normalized_to_pixels


def test_converts_normalized_2d_coordinates():
    points = np.array([[0.5, 0.25], [1.0, 1.0]], dtype=np.float32)

    pixels = normalized_to_pixels(points, image_width=640, image_height=480)

    np.testing.assert_allclose(pixels, [[320, 120], [640, 480]])


def test_converts_normalized_3d_coordinates_and_scales_depth_by_width():
    points = np.array([[0.5, 0.25, -0.1]], dtype=np.float32)

    pixels = normalized_to_pixels(points, image_width=640, image_height=480)

    np.testing.assert_allclose(pixels, [[320, 120, -64]])


@pytest.mark.parametrize("width,height", [(0, 480), (640, 0), (-1, 480)])
def test_rejects_non_positive_image_dimensions(width, height):
    with pytest.raises(ValueError, match="dimensions must be positive"):
        normalized_to_pixels(np.array([[0.5, 0.5]]), width, height)


@pytest.mark.parametrize(
    "points",
    [
        np.array([]),
        np.zeros((2, 4)),
        np.zeros((2, 1)),
        np.array([[np.nan, 0.5]]),
        np.array([[0.5, np.inf]]),
    ],
)
def test_rejects_invalid_landmarks(points):
    with pytest.raises(ValueError):
        normalized_to_pixels(points, 640, 480)


def test_does_not_mutate_input():
    points = np.array([[0.5, 0.25, 0.1]], dtype=np.float32)
    original = points.copy()

    normalized_to_pixels(points, 640, 480)

    np.testing.assert_array_equal(points, original)
