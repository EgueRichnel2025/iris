import numpy as np
import pytest

from iris.qt_quick_glasses import decompose_face_transform


def test_decompose_identity_face_transform_returns_expected_pose():
    position, rotation = decompose_face_transform(np.eye(4, dtype=np.float32))
    assert position.x() == pytest.approx(0.0)
    assert position.y() == pytest.approx(0.0)
    assert position.z() == pytest.approx(0.0)
    assert rotation.x() == pytest.approx(0.0, abs=1e-4)
    assert rotation.y() == pytest.approx(0.0, abs=1e-4)
    assert rotation.z() == pytest.approx(0.0, abs=1e-4)


def test_decompose_face_transform_preserves_mediapipe_translation():
    matrix = np.eye(4, dtype=np.float32)
    matrix[:3, 3] = (2.5, -8.4, -26.4)
    position, _ = decompose_face_transform(matrix)
    assert position.x() == pytest.approx(2.5)
    assert position.y() == pytest.approx(-8.4)
    assert position.z() == pytest.approx(-26.4)


def test_decompose_face_transform_converts_yaw_rotation():
    angle = np.deg2rad(25.0)
    matrix = np.eye(4, dtype=np.float32)
    matrix[:3, :3] = [
        [np.cos(angle), 0.0, np.sin(angle)],
        [0.0, 1.0, 0.0],
        [-np.sin(angle), 0.0, np.cos(angle)],
    ]
    _, rotation = decompose_face_transform(matrix)
    assert abs(rotation.y()) == pytest.approx(25.0, abs=0.2)


def test_decompose_face_transform_rejects_degenerate_rotation():
    matrix = np.eye(4, dtype=np.float32)
    matrix[:3, :3] = 0.0
    with pytest.raises(ValueError, match="degenerate scale"):
        decompose_face_transform(matrix)
