"""Unit tests for the local image effects."""

import numpy as np
import pytest

from iris.effects import EFFECTS, apply_effect, enhance_camera_lighting


@pytest.mark.parametrize("effect,_label", EFFECTS)
def test_every_effect_returns_same_sized_bgr_frame(effect: str, _label: str) -> None:
    frame = np.full((80, 120, 3), 110, dtype=np.uint8)
    result = apply_effect(frame, effect)

    assert result.shape == frame.shape
    assert result.dtype == np.uint8
    assert result is not frame


def test_original_effect_preserves_pixel_values() -> None:
    frame = np.zeros((12, 16, 3), dtype=np.uint8)
    frame[2, 3] = (10, 80, 220)

    result = apply_effect(frame, "original")

    np.testing.assert_array_equal(result, frame)


def test_unknown_effect_is_rejected() -> None:
    frame = np.zeros((8, 8, 3), dtype=np.uint8)

    with pytest.raises(ValueError, match="Unknown effect"):
        apply_effect(frame, "not-a-filter")


def test_empty_frame_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        apply_effect(np.array([]), "original")


def test_camera_lighting_enhancement_preserves_shape_and_dtype() -> None:
    frame = np.full((120, 160, 3), 35, dtype=np.uint8)
    result = enhance_camera_lighting(frame)
    assert result.shape == frame.shape
    assert result.dtype == np.uint8
    assert result.mean() > frame.mean()
    np.testing.assert_array_equal(frame, np.full((120, 160, 3), 35, dtype=np.uint8))


def test_camera_lighting_enhancement_does_not_clip_uniform_white_frame() -> None:
    frame = np.full((80, 100, 3), 245, dtype=np.uint8)
    result = enhance_camera_lighting(frame)
    assert result.mean() >= 240
    assert result.max() <= 255


def test_camera_lighting_rejects_invalid_frame() -> None:
    with pytest.raises(ValueError, match="uint8 BGR"):
        enhance_camera_lighting(np.zeros((10, 10), dtype=np.uint8))
