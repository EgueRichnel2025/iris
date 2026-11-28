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



def test_glasses_pose_smoothing_interpolates_translation_and_rotation():
    from iris.qt_quick_glasses import FacePoseSmoother

    smoother = FacePoseSmoother(alpha=0.35)
    first = np.eye(4, dtype=np.float32)
    first[:3, 3] = (0.0, -0.36, -33.17)
    smoother.update(first)

    second = np.eye(4, dtype=np.float32)
    second[:3, 3] = (10.0, 3.64, -23.17)
    position, rotation = smoother.update(second)

    assert position.x() == pytest.approx(3.5)
    assert position.y() == pytest.approx(1.4)
    assert position.z() == pytest.approx(-26.5, abs=1e-5)
    assert rotation.y() == pytest.approx(0.0, abs=0.3)


def test_glasses_pose_smoothing_resets_when_face_is_lost():
    from iris.qt_quick_glasses import FacePoseSmoother

    smoother = FacePoseSmoother()
    smoother.update(np.eye(4, dtype=np.float32))
    assert smoother.position is not None
    assert smoother.rotation is not None
    assert smoother.update(None) is None
    assert smoother.position is None
    assert smoother.rotation is None
