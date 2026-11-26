"""Resolve bundled model assets in source and frozen applications."""

from __future__ import annotations

import sys
from pathlib import Path


def face_landmarker_model_path() -> Path:
    """Return the expected local Face Landmarker model path.

    PyInstaller extracts bundled data under sys._MEIPASS. In source mode the
    model lives in desktop/assets/models relative to the desktop project root.
    """
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root is not None:
        root = Path(bundle_root)
    else:
        root = Path(__file__).resolve().parents[2]
    return root / "assets" / "models" / "face_landmarker.task"
