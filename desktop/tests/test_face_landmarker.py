from __future__ import annotations

import sys
from types import ModuleType, SimpleNamespace

import numpy as np
import pytest

from iris.vision.face_landmarker import FaceLandmarker


class FakeTask:
    def __init__(self, result=None):
        self.result = result or SimpleNamespace(face_landmarks=[])
        self.frames = []
        self.closed = False

    def detect_for_video(self, image, timestamp_ms):
        self.frames.append((image, timestamp_ms))
        return self.result

    def close(self):
        self.closed = True


def install_fake_mediapipe(monkeypatch, task):
    points = [SimpleNamespace(x=0.25, y=0.5, z=-0.1)]
    result = SimpleNamespace(face_landmarks=[points])
    task.result = result
    vision = SimpleNamespace(
        RunningMode=SimpleNamespace(VIDEO="VIDEO"),
        FaceLandmarkerOptions=lambda **kwargs: kwargs,
        FaceLandmarker=SimpleNamespace(create_from_options=lambda options: task),
    )
    fake = ModuleType("mediapipe")
    fake.tasks = SimpleNamespace(
        BaseOptions=lambda **kwargs: kwargs,
        vision=vision,
    )
    fake.ImageFormat = SimpleNamespace(SRGB="SRGB")
    fake.Image = lambda **kwargs: SimpleNamespace(**kwargs)
    monkeypatch.setitem(sys.modules, "mediapipe", fake)


def test_open_requires_existing_model(tmp_path):
    detector = FaceLandmarker(tmp_path / "missing.task")
    with pytest.raises(FileNotFoundError, match="model not found"):
        detector.open()


def test_open_rejects_zero_faces(tmp_path):
    model = tmp_path / "face.task"
    model.touch()
    detector = FaceLandmarker(model, num_faces=0)
    with pytest.raises(ValueError, match="num_faces"):
        detector.open()


def test_detect_requires_open_detector(tmp_path):
    detector = FaceLandmarker(tmp_path / "face.task")
    frame = np.zeros((8, 8, 3), dtype=np.uint8)
    with pytest.raises(RuntimeError, match="not open"):
        detector.detect(frame, 1)


def test_open_reports_missing_mediapipe(tmp_path, monkeypatch):
    model = tmp_path / "face.task"
    model.touch()
    monkeypatch.setitem(sys.modules, "mediapipe", None)
    detector = FaceLandmarker(model)
    with pytest.raises(RuntimeError, match="MediaPipe is not installed"):
        detector.open()


def test_detect_returns_normalized_landmarks(tmp_path, monkeypatch):
    model = tmp_path / "face.task"
    model.touch()
    task = FakeTask()
    install_fake_mediapipe(monkeypatch, task)
    detector = FaceLandmarker(model)
    detector.open()

    result = detector.detect(np.zeros((10, 12, 3), dtype=np.uint8), 100)

    assert result.timestamp_ms == 100
    assert result.face_count == 1
    np.testing.assert_allclose(result.faces[0], [[0.25, 0.5, -0.1]])
    assert result.faces[0].dtype == np.float32


def test_detect_converts_bgr_frame_to_rgb(tmp_path, monkeypatch):
    model = tmp_path / "face.task"
    model.touch()
    task = FakeTask()
    install_fake_mediapipe(monkeypatch, task)
    detector = FaceLandmarker(model)
    detector.open()
    frame = np.array([[[10, 20, 30]]], dtype=np.uint8)

    detector.detect(frame, 1)

    np.testing.assert_array_equal(task.frames[0][0].data, [[[30, 20, 10]]])
    assert task.frames[0][0].image_format == "SRGB"


@pytest.mark.parametrize(
    "frame",
    [
        np.zeros((8, 8), dtype=np.uint8),
        np.zeros((8, 8, 4), dtype=np.uint8),
        np.zeros((0, 8, 3), dtype=np.uint8),
        np.zeros((8, 8, 3), dtype=np.float32),
    ],
)
def test_detect_rejects_invalid_frames(tmp_path, monkeypatch, frame):
    model = tmp_path / "face.task"
    model.touch()
    task = FakeTask()
    install_fake_mediapipe(monkeypatch, task)
    detector = FaceLandmarker(model)
    detector.open()

    with pytest.raises(ValueError):
        detector.detect(frame, 1)


def test_video_timestamps_must_increase(tmp_path, monkeypatch):
    model = tmp_path / "face.task"
    model.touch()
    task = FakeTask()
    install_fake_mediapipe(monkeypatch, task)
    detector = FaceLandmarker(model)
    detector.open()
    frame = np.zeros((8, 8, 3), dtype=np.uint8)
    detector.detect(frame, 20)

    with pytest.raises(ValueError, match="must increase"):
        detector.detect(frame, 20)


def test_close_is_idempotent_and_resets_timestamp(tmp_path, monkeypatch):
    model = tmp_path / "face.task"
    model.touch()
    task = FakeTask()
    install_fake_mediapipe(monkeypatch, task)
    detector = FaceLandmarker(model)
    detector.open()
    detector.detect(np.zeros((8, 8, 3), dtype=np.uint8), 20)

    detector.close()
    detector.close()

    assert task.closed
    assert not detector.is_open
