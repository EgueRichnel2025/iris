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


class FakeVisionPipeline:
    def __init__(self):
        self.opened = False
        self.closed = False
        self.timestamps = []

    def open(self):
        self.opened = True

    def process(self, frame, timestamp_ms):
        self.timestamps.append(timestamp_ms)
        landmarks = np.array([[0.5, 0.5, 0.0]], dtype=np.float32)
        return SimpleNamespace(face_count=1, smoothed_faces=(landmarks,))

    def close(self):
        self.closed = True


def test_camera_thread_runs_face_pipeline_and_releases_resources(monkeypatch):
    capture = FakeCapture()
    pipeline = FakeVisionPipeline()
    monkeypatch.setattr(camera_module.cv2, "VideoCapture", lambda *_args: capture)
    monkeypatch.setattr(camera_module.time, "monotonic_ns", iter([1_000_000, 2_000_000]).__next__)

    camera = CameraThread(vision_pipeline=pipeline)
    detected_counts = []
    camera.face_count_updated.connect(detected_counts.append)

    camera.run()

    assert pipeline.opened
    assert pipeline.closed
    assert capture.released
    assert pipeline.timestamps == [1, 2]
    assert detected_counts == [1, 1]


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
