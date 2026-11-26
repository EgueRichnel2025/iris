import cv2
import numpy as np
import pytest

from iris.vision.head_pose import HeadPoseEstimator


MODEL_POINTS = np.array(
    [
        (0.0, 0.0, 0.0),
        (0.0, 330.0, 65.0),
        (-225.0, -170.0, 135.0),
        (225.0, -170.0, 135.0),
        (-150.0, 150.0, 125.0),
        (150.0, 150.0, 125.0),
    ],
    dtype=np.float64,
)
LANDMARK_IDS = (1, 152, 33, 263, 61, 291)
WIDTH, HEIGHT = 640, 480
CAMERA_MATRIX = np.array(
    [[WIDTH, 0, WIDTH / 2], [0, WIDTH, HEIGHT / 2], [0, 0, 1]],
    dtype=np.float64,
)


def make_landmarks(yaw=0.0, pitch=0.0, roll=0.0):
    yaw, pitch, roll = np.radians([yaw, pitch, roll])
    rx = np.array(
        [[1, 0, 0], [0, np.cos(pitch), -np.sin(pitch)],
         [0, np.sin(pitch), np.cos(pitch)]]
    )
    ry = np.array(
        [[np.cos(yaw), 0, np.sin(yaw)], [0, 1, 0],
         [-np.sin(yaw), 0, np.cos(yaw)]]
    )
    rz = np.array(
        [[np.cos(roll), -np.sin(roll), 0],
         [np.sin(roll), np.cos(roll), 0], [0, 0, 1]]
    )
    rotation = rz @ ry @ rx
    rotation_vector, _ = cv2.Rodrigues(rotation.astype(np.float64))
    translation = np.array([[0.0], [0.0], [1000.0]])
    image_points, _ = cv2.projectPoints(
        MODEL_POINTS, rotation_vector, translation, CAMERA_MATRIX, np.zeros((4, 1))
    )
    landmarks = np.zeros((478, 3), dtype=np.float64)
    for landmark_id, point in zip(LANDMARK_IDS, image_points.reshape(-1, 2)):
        landmarks[landmark_id, :2] = point / [WIDTH, HEIGHT]
    return landmarks


def test_estimates_neutral_head_pose():
    pose = HeadPoseEstimator().estimate(make_landmarks(), WIDTH, HEIGHT)

    assert abs(pose.yaw) < 0.5
    assert abs(pose.pitch) < 0.5
    assert abs(pose.roll) < 0.5
    assert pose.rotation_vector.shape == (3,)
    assert pose.translation_vector.shape == (3,)


@pytest.mark.parametrize(
    "expected",
    [
        (20.0, 0.0, 0.0),
        (-20.0, 0.0, 0.0),
        (0.0, 15.0, 0.0),
        (0.0, -15.0, 0.0),
        (0.0, 0.0, 12.0),
        (0.0, 0.0, -12.0),
    ],
)
def test_recovers_individual_head_rotation_axes(expected):
    landmarks = make_landmarks(*expected)

    pose = HeadPoseEstimator().estimate(landmarks, WIDTH, HEIGHT)

    np.testing.assert_allclose(
        [pose.yaw, pose.pitch, pose.roll], expected, atol=0.2
    )


def test_rejects_non_positive_image_dimensions():
    with pytest.raises(ValueError, match="dimensions"):
        HeadPoseEstimator().estimate(make_landmarks(), 0, HEIGHT)


def test_rejects_missing_required_landmarks():
    with pytest.raises(ValueError, match="required face points"):
        HeadPoseEstimator().estimate(np.zeros((100, 3)), WIDTH, HEIGHT)


def test_rejects_invalid_landmark_shapes_and_non_finite_values():
    estimator = HeadPoseEstimator()
    with pytest.raises(ValueError, match="shape"):
        estimator.estimate(np.zeros((478, 4)), WIDTH, HEIGHT)

    points = make_landmarks()
    points[1, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        estimator.estimate(points, WIDTH, HEIGHT)



@pytest.mark.parametrize(
    "expected",
    [
        (0.0, 0.0, 0.0),
        (20.0, 0.0, 0.0),
        (-20.0, 0.0, 0.0),
        (0.0, 15.0, 0.0),
        (0.0, -15.0, 0.0),
        (0.0, 0.0, 12.0),
        (0.0, 0.0, -12.0),
        (10.0, -6.0, 4.0),
    ],
)
def test_estimates_pose_from_horizontally_mirrored_landmarks(expected):
    landmarks = make_landmarks(*expected)
    landmarks[:, 0] = 1.0 - landmarks[:, 0]

    pose = HeadPoseEstimator().estimate(
        landmarks, WIDTH, HEIGHT, mirrored_input=True
    )

    np.testing.assert_allclose(
        [pose.yaw, pose.pitch, pose.roll], expected, atol=0.2
    )
