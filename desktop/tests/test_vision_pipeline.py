from types import SimpleNamespace

import numpy as np
import pytest

from iris.vision.pipeline import FaceVisionPipeline


class FakeDetector:
    def __init__(self, faces_by_frame):
        self.faces_by_frame = iter(faces_by_frame)
        self.opened = False
        self.closed = False

    def open(self):
        self.opened = True

    def detect(self, frame, timestamp_ms):
        return SimpleNamespace(timestamp_ms=timestamp_ms, faces=next(self.faces_by_frame))

    def close(self):
        self.closed = True


def test_pipeline_requires_open_before_processing():
    pipeline = FaceVisionPipeline(FakeDetector([]))

    with pytest.raises(RuntimeError, match="not open"):
        pipeline.process(np.zeros((2, 2, 3), dtype=np.uint8), 1)


def test_pipeline_opens_detector_and_smooths_landmarks():
    first = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)
    second = np.array([[1.0, 1.0, 1.0]], dtype=np.float32)
    detector = FakeDetector([(first,), (second,)])
    pipeline = FaceVisionPipeline(detector, smoother_alpha=0.5)
    pipeline.open()

    first_result = pipeline.process(np.zeros((2, 2, 3), dtype=np.uint8), 1)
    second_result = pipeline.process(np.zeros((2, 2, 3), dtype=np.uint8), 2)

    assert detector.opened
    assert first_result.face_count == 1
    np.testing.assert_array_equal(first_result.smoothed_faces[0], first)
    np.testing.assert_allclose(second_result.smoothed_faces[0], [[0.5, 0.5, 0.5]])


def test_lost_face_resets_smoothing_history():
    first = np.array([[0.2, 0.2, 0.2]], dtype=np.float32)
    moved = np.array([[0.8, 0.8, 0.8]], dtype=np.float32)
    detector = FakeDetector([(first,), (), (moved,)])
    pipeline = FaceVisionPipeline(detector, smoother_alpha=0.1)
    pipeline.open()

    pipeline.process(np.zeros((2, 2, 3), dtype=np.uint8), 1)
    lost = pipeline.process(np.zeros((2, 2, 3), dtype=np.uint8), 2)
    reacquired = pipeline.process(np.zeros((2, 2, 3), dtype=np.uint8), 3)

    assert lost.face_count == 0
    assert lost.smoothed_faces == ()
    np.testing.assert_array_equal(reacquired.smoothed_faces[0], moved)


def test_pipeline_closes_detector_and_can_be_closed_twice():
    detector = FakeDetector([])
    pipeline = FaceVisionPipeline(detector)
    pipeline.open()

    pipeline.close()
    pipeline.close()

    assert detector.closed
    assert not pipeline.is_open


def test_pipeline_validates_smoothing_alpha():
    with pytest.raises(ValueError, match="smoother_alpha"):
        FaceVisionPipeline(FakeDetector([]), smoother_alpha=1.5)
