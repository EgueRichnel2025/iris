"""Unit tests for the local image effects."""

import numpy as np
import pytest

from iris.effects import EFFECTS, apply_effect


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
