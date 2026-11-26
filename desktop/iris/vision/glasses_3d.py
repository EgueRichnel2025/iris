"""Optional VTK-backed loading of glTF 2.0 glasses accessories."""

from __future__ import annotations

import json
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_GLTF_MAGIC = b"glTF"
_JSON_CHUNK = 0x4E4F534A


class Glasses3DAssetError(ValueError):
    """Raised when a glasses model is not a valid binary glTF asset."""


def read_glb_document(model_path: str | Path) -> dict[str, Any]:
    """Read and validate the JSON chunk of a binary glTF 2.0 asset."""
    path = Path(model_path)
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise Glasses3DAssetError(f"Cannot read 3D accessory: {path}") from exc

    if len(data) < 20:
        raise Glasses3DAssetError("GLB file is too small to contain a JSON chunk")

    magic, version, declared_length = struct.unpack_from("<4sII", data, 0)
    if magic != _GLTF_MAGIC or version != 2:
        raise Glasses3DAssetError("Accessory must be a binary glTF 2.0 file")
    if declared_length != len(data):
        raise Glasses3DAssetError("GLB declared length does not match file size")

    chunk_length, chunk_type = struct.unpack_from("<II", data, 12)
    if chunk_type != _JSON_CHUNK or 20 + chunk_length > len(data):
        raise Glasses3DAssetError("GLB does not start with a valid JSON chunk")

    try:
        document = json.loads(data[20 : 20 + chunk_length].decode("utf-8").rstrip(" \t\r\n\0"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Glasses3DAssetError("GLB JSON chunk is invalid") from exc

    if document.get("asset", {}).get("version") != "2.0":
        raise Glasses3DAssetError("GLB asset metadata must declare glTF 2.0")
    if not document.get("meshes"):
        raise Glasses3DAssetError("3D accessory contains no meshes")
    return document


@dataclass(slots=True)
class Glasses3DScene:
    """Keep VTK objects alive for the lifetime of the embedded widget."""

    widget: Any
    renderer: Any
    reader: Any
    actor: Any
    initialized: bool = False
    image_importer: Any = None
    image_actor: Any = None


def create_glasses_3d_scene(model_path: str | Path, parent: Any = None) -> Glasses3DScene:
    """Create a PySide6-compatible VTK widget and load a GLB accessory."""
    path = Path(model_path)
    read_glb_document(path)

    try:
        from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
        from vtkmodules.vtkIOGeometry import vtkGLTFReader
        from vtkmodules.vtkRenderingCore import (
            vtkActor,
            vtkCompositePolyDataMapper,
            vtkRenderer,
        )
    except ImportError as exc:
        raise RuntimeError(
            "3D accessories require the optional 'ar3d' dependencies (VTK)"
        ) from exc

    widget = QVTKRenderWindowInteractor(parent)
    reader = vtkGLTFReader()
    reader.SetFileName(str(path))
    reader.Update()
    if reader.GetOutput().GetNumberOfBlocks() == 0:
        raise Glasses3DAssetError("VTK could not load any geometry from the GLB model")

    renderer = vtkRenderer()
    renderer.SetBackground(0.035, 0.055, 0.085)
    renderer.SetLayer(0)
    mapper = vtkCompositePolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    renderer.AddActor(actor)
    actor.SetVisibility(False)

    render_window = widget.GetRenderWindow()
    render_window.SetNumberOfLayers(2)
    render_window.AddRenderer(renderer)

    try:
        from vtkmodules.vtkIOImage import vtkImageImport
        from vtkmodules.vtkRenderingCore import vtkImageActor, vtkRenderer
    except ImportError as exc:
        raise RuntimeError("VTK image rendering modules are unavailable") from exc

    background = vtkRenderer()
    background.SetLayer(0)
    background.InteractiveOff()
    background.SetActiveCamera(renderer.GetActiveCamera())
    render_window.AddRenderer(background)
    importer = vtkImageImport()
    image_actor = vtkImageActor()
    image_actor.GetMapper().SetInputConnection(importer.GetOutputPort())
    background.AddActor(image_actor)
    renderer.SetLayer(1)
    renderer.SetPreserveColorBuffer(True)

    return Glasses3DScene(
        widget=widget, renderer=renderer, reader=reader, actor=actor,
        image_importer=importer, image_actor=image_actor,
    )


def initialize_glasses_3d_scene(scene: Glasses3DScene) -> None:
    """Initialize VTK only after its Qt widget has been shown."""
    if scene.initialized:
        return
    scene.widget.Initialize()
    scene.widget.GetRenderWindow().Render()
    scene.initialized = True


def update_glasses_video_frame(scene: Glasses3DScene, frame_rgb: Any) -> None:
    """Update the video background behind the 3D glasses in the same render."""
    import numpy as np

    frame = np.asarray(frame_rgb, dtype=np.uint8)
    if frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError("video frame must be an RGB image with three channels")
    height, width, _ = frame.shape
    importer = scene.image_importer
    if importer is None:
        raise RuntimeError("video background is not configured")
    # VTK image data starts at the lower-left; camera frames start at the top-left.
    bottom_up = np.ascontiguousarray(frame[::-1])
    importer.SetDataScalarTypeToUnsignedChar()
    importer.SetNumberOfScalarComponents(3)
    importer.SetWholeExtent(0, width - 1, 0, height - 1, 0, 0)
    importer.SetDataExtentToWholeExtent()
    importer.CopyImportVoidPointer(bottom_up.tobytes(), bottom_up.nbytes)
    importer.Update()

    # Put the video plane 100 cm from the virtual camera and use a calibrated
    # pinhole approximation (focal length 900 px) for the initial preview.
    focal_px = float(max(width, height)) * 1.25
    distance_cm = 100.0
    plane_width = width * distance_cm / focal_px
    plane_height = height * distance_cm / focal_px
    scene.image_actor.SetPosition(-plane_width / 2, -plane_height / 2, -distance_cm)
    scene.image_actor.SetScale(plane_width / width, plane_height / height, 1.0)

    camera = scene.renderer.GetActiveCamera()
    camera.SetPosition(0.0, 0.0, 0.0)
    camera.SetFocalPoint(0.0, 0.0, -1.0)
    camera.SetViewUp(0.0, 1.0, 0.0)
    camera.SetViewAngle(2.0 * np.degrees(np.arctan(height / (2.0 * focal_px))))
    camera.SetClippingRange(0.1, 500.0)
    scene.image_importer.Modified()
    if scene.initialized:
        scene.widget.GetRenderWindow().Render()
