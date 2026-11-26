"""Available face-anchored AR accessories."""

from __future__ import annotations

from typing import Final

import numpy as np
from numpy.typing import NDArray

from iris.vision.glasses import draw_glasses


ACCESSORIES: Final[tuple[tuple[str, str], ...]] = (
    ("none", "Aucun accessoire"),
    ("glasses", "Lunettes"),
)


def apply_accessory(
    frame_bgr: NDArray[np.uint8],
    accessory: str,
    faces: tuple[NDArray[np.float32], ...],
) -> NDArray[np.uint8]:
    """Apply the selected accessory to the first detected face."""
    if accessory == "none":
        return frame_bgr.copy()
    if accessory == "glasses":
        if not faces:
            return frame_bgr.copy()
        return draw_glasses(frame_bgr, faces[0])
    raise ValueError(f"Unknown accessory: {accessory}")
