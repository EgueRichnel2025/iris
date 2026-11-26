import numpy as np
import pytest

from iris.accessories import ACCESSORIES, apply_accessory


def face_landmarks():
    points = np.full((478, 3), 0.5, dtype=np.float32)
    points[33] = (0.35, 0.42, 0.0)
    points[133] = (0.45, 0.42, 0.0)
    points[263] = (0.65, 0.42, 0.0)
    points[362] = (0.55, 0.42, 0.0)
    return points


def test_accessory_catalog_contains_none_and_glasses():
    assert ACCESSORIES == (
        ("none", "Aucun accessoire"),
        ("glasses", "Lunettes"),
    )


def test_none_accessory_returns_an_independent_frame_copy():
    frame = np.zeros((100, 160, 3), dtype=np.uint8)

    output = apply_accessory(frame, "none", (face_landmarks(),))

    assert output is not frame
    np.testing.assert_array_equal(output, frame)


def test_glasses_accessory_is_rendered_when_face_is_available():
    frame = np.zeros((240, 320, 3), dtype=np.uint8)

    output = apply_accessory(frame, "glasses", (face_landmarks(),))

    assert np.count_nonzero(output) > 0
    assert np.count_nonzero(frame) == 0


def test_glasses_are_not_rendered_without_a_face():
    frame = np.zeros((100, 160, 3), dtype=np.uint8)

    output = apply_accessory(frame, "glasses", ())

    np.testing.assert_array_equal(output, frame)


def test_unknown_accessory_is_rejected():
    with pytest.raises(ValueError, match="Unknown accessory"):
        apply_accessory(np.zeros((10, 10, 3), dtype=np.uint8), "hat", ())
