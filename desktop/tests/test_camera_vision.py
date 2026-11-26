from types import SimpleNamespace

import numpy as np

from iris import camera as camera_module
from iris.camera import CameraThread


class FakeCapture:
    def __init__(self, *_args):
        self.frames = [
            np.zeros((32, 48, 3), dtype=np.uint8),
            np.zeros((32, 48, 3), dtype=np.uint8),
        ]
        self.released = False

    def isOpened(self):
        return True

    def set(self, *_args):
        return True

    def read(self):
        if self.frames:
            return True, self.frames.pop(0)
        return False, None

    def release(self):
        self.released = True


class FakePoseEstimator:
    def __init__(self, error=None):
        self.error = error
        self.calls = []

    def estimate(self, landmarks, width, height):
        self.calls.append((landmarks, width, height))
        if self.error:
            raise self.error
        return SimpleNamespace(yaw=12.0, pitch=-4.0, roll=3.0)


class FakeVisionPipeline:
    def __init__(self):
        self.opened = False
        self.closed = False
        self.timestamps = []

    def open(self):
        self.opened = True

    def process(self, frame, timestamp_ms):
        self.timestamps.append(timestamp_ms)
        landmarks = np.zeros((478, 3), dtype=np.float32)
        landmarks[:, :2] = 0.5
        return SimpleNamespace(face_count=1, smoothed_faces=(landmarks,))

    def close(self):
        self.closed = True


def test_camera_thread_runs_face_pipeline_and_releases_resources(monkeypatch):
    capture = FakeCapture()
    pipeline = FakeVisionPipeline()
    monkeypatch.setattr(camera_module.cv2, "VideoCapture", lambda *_args: capture)
    monkeypatch.setattr(camera_module.time, "monotonic_ns", iter([1_000_000, 2_000_000]).__next__)

    pose_estimator = FakePoseEstimator()
    camera = CameraThread(vision_pipeline=pipeline, pose_estimator=pose_estimator)
    detected_counts = []
    poses = []
    camera.face_count_updated.connect(detected_counts.append)
    camera.head_pose_updated.connect(lambda yaw, pitch, roll: poses.append((yaw, pitch, roll)))

    camera.run()

    assert pipeline.opened
    assert pipeline.closed
    assert capture.released
    assert pipeline.timestamps == [1, 2]
    assert detected_counts == [1, 1]
    assert poses == [(12.0, -4.0, 3.0), (12.0, -4.0, 3.0)]
    assert len(pose_estimator.calls) == 2


def test_camera_keeps_running_when_vision_initialization_fails(monkeypatch):
    capture = FakeCapture()
    monkeypatch.setattr(camera_module.cv2, "VideoCapture", lambda *_args: capture)

    class BrokenPipeline:
        def open(self):
            raise RuntimeError("model unavailable")

    camera = CameraThread(vision_pipeline=BrokenPipeline())
    errors = []
    camera.vision_error.connect(errors.append)

    camera.run()

    assert capture.released
    assert len(errors) == 1
    assert "model unavailable" in errors[0]



def test_pose_failure_does_not_stop_face_detection(monkeypatch):
    capture = FakeCapture()
    pipeline = FakeVisionPipeline()
    pose_estimator = FakePoseEstimator(error=RuntimeError("unstable geometry"))
    monkeypatch.setattr(camera_module.cv2, "VideoCapture", lambda *_args: capture)
    monkeypatch.setattr(
        camera_module.time,
        "monotonic_ns",
        iter([1_000_000, 2_000_000]).__next__,
    )

    camera = CameraThread(
        vision_pipeline=pipeline,
        pose_estimator=pose_estimator,
    )
    detected_counts = []
    poses = []
    errors = []
    camera.face_count_updated.connect(detected_counts.append)
    camera.head_pose_updated.connect(
        lambda yaw, pitch, roll: poses.append((yaw, pitch, roll))
    )
    camera.vision_error.connect(errors.append)

    camera.run()

    assert pipeline.closed
    assert capture.released
    assert detected_counts == [1, 1]
    assert poses == [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)]
    assert len(errors) == 2
    assert all("Estimation de pose" in error for error in errors)



def test_camera_resets_pose_when_face_disappears(monkeypatch):
    capture = FakeCapture()

    class NoFacePipeline(FakeVisionPipeline):
        def process(self, frame, timestamp_ms):
            self.timestamps.append(timestamp_ms)
            return SimpleNamespace(face_count=0, smoothed_faces=())

    pipeline = NoFacePipeline()
    pose_estimator = FakePoseEstimator()
    monkeypatch.setattr(camera_module.cv2, "VideoCapture", lambda *_args: capture)
    monkeypatch.setattr(
        camera_module.time,
        "monotonic_ns",
        iter([1_000_000, 2_000_000]).__next__,
    )

    camera = CameraThread(
        vision_pipeline=pipeline,
        pose_estimator=pose_estimator,
    )
    detected_counts = []
    poses = []
    camera.face_count_updated.connect(detected_counts.append)
    camera.head_pose_updated.connect(
        lambda yaw, pitch, roll: poses.append((yaw, pitch, roll))
    )

    camera.run()

    assert detected_counts == [0, 0]
    assert poses == [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)]
    assert pose_estimator.calls == []
    assert pipeline.closed
    assert capture.released
