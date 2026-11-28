"""Qt Quick 3D camera compositor for the GLB glasses accessory."""
from __future__ import annotations
import threading
from pathlib import Path
import numpy as np
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QImage, QQuaternion, QVector3D
from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtQuickWidgets import QQuickWidget
from iris.vision.face_transform import face_model_anchor_position

class CameraImageProvider(QQuickImageProvider):
    """Serve the latest camera image to QML without temporary files."""
    def __init__(self):
        super().__init__(QQuickImageProvider.ImageType.Image)
        self._lock = threading.Lock()
        self._image = QImage(1, 1, QImage.Format.Format_RGB888)
        self._image.fill(Qt.GlobalColor.black)
    def set_image(self, image):
        with self._lock:
            self._image = image.copy()
    def requestImage(self, _image_id, size, requested_size):  # noqa: N802
        with self._lock:
            image = self._image.copy()
        if requested_size.isValid():
            image = image.scaled(requested_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        if size is not None:
            size.setWidth(image.width())
            size.setHeight(image.height())
        return image

def _quaternion_from_rotation(matrix: np.ndarray) -> QQuaternion:
    trace = float(np.trace(matrix))
    if trace > 0:
        scale = np.sqrt(trace + 1.0) * 2.0
        w, x, y, z = 0.25 * scale, (matrix[2,1]-matrix[1,2])/scale, (matrix[0,2]-matrix[2,0])/scale, (matrix[1,0]-matrix[0,1])/scale
    elif matrix[0,0] > matrix[1,1] and matrix[0,0] > matrix[2,2]:
        scale = np.sqrt(1.0 + matrix[0,0] - matrix[1,1] - matrix[2,2]) * 2.0
        w, x, y, z = (matrix[2,1]-matrix[1,2])/scale, 0.25*scale, (matrix[0,1]+matrix[1,0])/scale, (matrix[0,2]+matrix[2,0])/scale
    elif matrix[1,1] > matrix[2,2]:
        scale = np.sqrt(1.0 + matrix[1,1] - matrix[0,0] - matrix[2,2]) * 2.0
        w, x, y, z = (matrix[0,2]-matrix[2,0])/scale, (matrix[0,1]+matrix[1,0])/scale, 0.25*scale, (matrix[1,2]+matrix[2,1])/scale
    else:
        scale = np.sqrt(1.0 + matrix[2,2] - matrix[0,0] - matrix[1,1]) * 2.0
        w, x, y, z = (matrix[1,0]-matrix[0,1])/scale, (matrix[0,2]+matrix[2,0])/scale, (matrix[1,2]+matrix[2,1])/scale, 0.25*scale
    result = QQuaternion(float(w), float(x), float(y), float(z))
    result.normalize()
    return result

def decompose_face_transform(facial_transformation_matrix):
    matrix = np.asarray(facial_transformation_matrix, dtype=np.float64)
    if matrix.shape != (4, 4) or not np.isfinite(matrix).all():
        raise ValueError("facial_transformation_matrix must be a finite 4x4 matrix")
    basis = matrix[:3, :3]
    scales = np.linalg.norm(basis, axis=0)
    if np.any(scales <= 1e-8):
        raise ValueError("face transform contains a degenerate scale")
    rotation = basis / scales[np.newaxis, :]
    u, _, vt = np.linalg.svd(rotation)
    rotation = u @ vt
    if np.linalg.det(rotation) < 0:
        u[:, -1] *= -1
        rotation = u @ vt
    quaternion = _quaternion_from_rotation(rotation)
    return QVector3D(*(float(value) for value in matrix[:3, 3])), quaternion.toEulerAngles()


class FacePoseSmoother:
    """Smooth face translation and orientation without changing model scale."""

    def __init__(self, alpha: float = 0.35):
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be in (0, 1]")
        self.alpha = float(alpha)
        self.position = None
        self.rotation = None

    def reset(self):
        self.position = None
        self.rotation = None

    def update(self, matrix):
        if matrix is None:
            self.reset()
            return None
        _, _ = decompose_face_transform(matrix)
        anchored_position = face_model_anchor_position(matrix)
        position = QVector3D(*(float(value) for value in anchored_position))
        basis = np.asarray(matrix, dtype=np.float64)[:3, :3]
        scales = np.linalg.norm(basis, axis=0)
        basis = basis / scales[np.newaxis, :]
        u, _, vt = np.linalg.svd(basis)
        rotation_matrix = u @ vt
        if np.linalg.det(rotation_matrix) < 0:
            u[:, -1] *= -1
            rotation_matrix = u @ vt
        current_rotation = _quaternion_from_rotation(rotation_matrix)

        if self.position is None or self.rotation is None:
            self.position = position
            self.rotation = current_rotation
        else:
            previous = self.position
            self.position = QVector3D(
                previous.x() + self.alpha * (position.x() - previous.x()),
                previous.y() + self.alpha * (position.y() - previous.y()),
                previous.z() + self.alpha * (position.z() - previous.z()),
            )
            self.rotation = QQuaternion.slerp(
                self.rotation, current_rotation, self.alpha
            )
            self.rotation.normalize()
        return self.position, self.rotation.toEulerAngles()

class GlassesQuickView(QQuickWidget):
    """Display camera frames and a face-anchored GLB model in one Qt view."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._provider = CameraImageProvider()
        self.engine().addImageProvider("camera", self._provider)
        self._frame_number = 0
        self._pose_smoother = FacePoseSmoother(alpha=0.35)
        self.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.setClearColor(Qt.GlobalColor.black)
        desktop_root = Path(__file__).resolve().parents[1]
        qml_path = desktop_root / "iris" / "ui" / "qml" / "glasses_view.qml"
        model_path = desktop_root / "assets" / "models" / "accessories" / "rectangular-acetate-glasses.glb"
        if not qml_path.is_file() or not model_path.is_file():
            raise FileNotFoundError("IRIS Quick 3D QML or GLB model asset is missing")
        self.setSource(QUrl.fromLocalFile(str(qml_path)))
        if self.status() == QQuickWidget.Status.Error:
            errors = "; ".join(error.toString() for error in self.errors())
            raise RuntimeError(f"Cannot load IRIS Quick 3D view: {errors}")
        self.rootObject().setProperty("modelSource", QUrl.fromLocalFile(str(model_path)))
        self.rootObject().setProperty("frameSource", "image://camera/frame/0")
    def set_video_frame(self, frame_rgb: np.ndarray):
        frame = np.asarray(frame_rgb)
        if frame.ndim != 3 or frame.shape[2] != 3 or frame.dtype != np.uint8:
            raise ValueError("frame_rgb must be an HxWx3 uint8 RGB image")
        height, width, _ = frame.shape
        image = QImage(np.ascontiguousarray(frame).data, width, height, width*3, QImage.Format.Format_RGB888).copy()
        self._provider.set_image(image)
        self._frame_number += 1
        self.rootObject().setProperty("frameSource", f"image://camera/frame/{self._frame_number}")
    def set_face_transform(self, matrix):
        root = self.rootObject()
        pose = self._pose_smoother.update(matrix)
        if pose is None:
            root.setProperty("hasFace", False)
            return
        position, rotation = pose
        root.setProperty("facePosition", position)
        root.setProperty("faceEulerRotation", rotation)
        root.setProperty("hasFace", True)
    def set_glasses_enabled(self, enabled: bool):
        self.rootObject().setProperty("glassesEnabled", bool(enabled))
