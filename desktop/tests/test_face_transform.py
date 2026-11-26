import numpy as np
import pytest

from iris.vision.face_transform import (
    GLB_METERS_TO_MEDIAPIPE_CENTIMETERS,
    build_face_actor_matrix,
)


def test_identity_face_pose_converts_glb_meters_to_centimeters():
    result = build_face_actor_matrix(np.eye(4))

    np.testing.assert_allclose(
        result,
        np.diag([100.0, 100.0, 100.0, 1.0]),
    )


def test_face_translation_is_preserved_after_model_unit_conversion():
    face = np.eye(4)
    face[:3, 3] = (2.5, -8.4, -26.4)

    result = build_face_actor_matrix(face)

    np.testing.assert_allclose(result[:3, 3], face[:3, 3])
    np.testing.assert_allclose(np.linalg.norm(result[:3, 0]), 100.0)


def test_face_rotation_is_applied_to_scaled_model_axes():
    face = np.eye(4)
    face[:3, :3] = np.array(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    )

    result = build_face_actor_matrix(face)

    np.testing.assert_allclose(result[:3, :3], face[:3, :3] * 100.0)


def test_custom_model_unit_scale_is_supported():
    result = build_face_actor_matrix(np.eye(4), model_to_centimeters=1.0)

    np.testing.assert_allclose(result, np.eye(4))


@pytest.mark.parametrize(
    "matrix",
    [np.eye(3), np.zeros((4, 4)), np.full((4, 4), np.nan)],
)
def test_invalid_face_matrices_are_rejected(matrix):
    with pytest.raises(ValueError):
        build_face_actor_matrix(matrix)


@pytest.mark.parametrize("scale", [0.0, -1.0, np.inf, np.nan])
def test_invalid_model_unit_scales_are_rejected(scale):
    with pytest.raises(ValueError, match="model_to_centimeters"):
        build_face_actor_matrix(np.eye(4), model_to_centimeters=scale)


def test_non_affine_face_matrix_is_rejected():
    matrix = np.eye(4)
    matrix[3, 0] = 1.0

    with pytest.raises(ValueError, match="affine"):
        build_face_actor_matrix(matrix)


def test_glb_unit_conversion_constant_matches_meter_to_centimeter_ratio():
    assert GLB_METERS_TO_MEDIAPIPE_CENTIMETERS == 100.0


def test_apply_face_transform_updates_vtk_actor_without_rendering_uninitialized_widget():
    from types import SimpleNamespace

    from iris.vision.face_transform import apply_face_transform

    class Actor:
        matrix = None

        def SetUserMatrix(self, matrix):
            self.matrix = matrix

    class Widget:
        def GetRenderWindow(self):
            raise AssertionError("an uninitialized widget must not be rendered")

    actor = Actor()
    scene = SimpleNamespace(actor=actor, widget=Widget(), initialized=False)
    face = np.eye(4)
    face[:3, 3] = (1.0, 2.0, -30.0)

    apply_face_transform(scene, face)

    assert actor.matrix is not None
    np.testing.assert_allclose(
        [[actor.matrix.GetElement(r, c) for c in range(4)] for r in range(4)],
        build_face_actor_matrix(face),
    )
