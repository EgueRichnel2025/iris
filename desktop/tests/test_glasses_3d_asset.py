import json
import struct

import pytest

from iris.vision.glasses_3d import Glasses3DAssetError, read_glb_document


def make_glb(document: dict) -> bytes:
    payload = json.dumps(document, separators=(",", ":")).encode("utf-8")
    payload += b" " * ((4 - len(payload) % 4) % 4)
    chunk = struct.pack("<II", len(payload), 0x4E4F534A) + payload
    return struct.pack("<4sII", b"glTF", 2, 12 + len(chunk)) + chunk


def test_reads_valid_glb_document(tmp_path):
    document = {"asset": {"version": "2.0"}, "meshes": [{"primitives": []}]}
    path = tmp_path / "valid.glb"
    path.write_bytes(make_glb(document))

    assert read_glb_document(path)["asset"]["version"] == "2.0"


def test_rejects_invalid_magic(tmp_path):
    path = tmp_path / "invalid.glb"
    path.write_bytes(b"not-a-glb-file-at-all")

    with pytest.raises(Glasses3DAssetError, match="too small|binary glTF"):
        read_glb_document(path)


def test_rejects_inconsistent_declared_length(tmp_path):
    path = tmp_path / "truncated.glb"
    path.write_bytes(make_glb({"asset": {"version": "2.0"}, "meshes": [{}]})[:-1])

    with pytest.raises(Glasses3DAssetError, match="declared length"):
        read_glb_document(path)


def test_rejects_non_glb_v2(tmp_path):
    path = tmp_path / "v1.glb"
    payload = json.dumps({"asset": {"version": "1.0"}, "meshes": [{}]}).encode()
    payload += b" " * ((4 - len(payload) % 4) % 4)
    chunk = struct.pack("<II", len(payload), 0x4E4F534A) + payload
    path.write_bytes(struct.pack("<4sII", b"glTF", 1, 12 + len(chunk)) + chunk)

    with pytest.raises(Glasses3DAssetError, match="glTF 2.0"):
        read_glb_document(path)


def test_rejects_document_without_meshes(tmp_path):
    path = tmp_path / "empty.glb"
    path.write_bytes(make_glb({"asset": {"version": "2.0"}}))

    with pytest.raises(Glasses3DAssetError, match="no meshes"):
        read_glb_document(path)


def test_rejects_invalid_json_chunk(tmp_path):
    payload = b"{not-json}"
    payload += b" " * ((4 - len(payload) % 4) % 4)
    chunk = struct.pack("<II", len(payload), 0x4E4F534A) + payload
    path = tmp_path / "bad-json.glb"
    path.write_bytes(struct.pack("<4sII", b"glTF", 2, 12 + len(chunk)) + chunk)

    with pytest.raises(Glasses3DAssetError, match="JSON chunk is invalid"):
        read_glb_document(path)


def test_scene_is_not_initialized_before_qt_widget_is_shown():
    from iris.vision.glasses_3d import Glasses3DScene

    scene = Glasses3DScene(
        widget=object(), renderer=object(), reader=object(), actor=object()
    )

    assert scene.initialized is False


def test_video_background_rejects_non_rgb_frames():
    from types import SimpleNamespace

    import numpy as np

    from iris.vision.glasses_3d import update_glasses_video_frame

    scene = SimpleNamespace(image_importer=object())
    with pytest.raises(ValueError, match="RGB image"):
        update_glasses_video_frame(scene, np.zeros((12, 12), dtype=np.uint8))


def test_video_background_updates_vtk_importer_and_camera():
    from types import SimpleNamespace

    import numpy as np

    from iris.vision.glasses_3d import update_glasses_video_frame

    class Importer:
        def __init__(self):
            self.data = None
        def SetDataScalarTypeToUnsignedChar(self): pass
        def SetNumberOfScalarComponents(self, value): self.components = value
        def SetWholeExtent(self, *values): self.extent = values
        def SetDataExtentToWholeExtent(self): pass
        def CopyImportVoidPointer(self, data, size): self.data = (data, size)
        def Update(self): pass
        def Modified(self): pass

    class ImageActor:
        def SetPosition(self, *values): self.position = values
        def SetScale(self, *values): self.scale = values

    class Camera:
        def SetPosition(self, *values): self.position = values
        def SetFocalPoint(self, *values): self.focal_point = values
        def SetViewUp(self, *values): self.view_up = values
        def SetViewAngle(self, value): self.view_angle = value
        def SetClippingRange(self, *values): self.clipping_range = values

    importer, image_actor, camera = Importer(), ImageActor(), Camera()
    scene = SimpleNamespace(
        image_importer=importer,
        image_actor=image_actor,
        renderer=SimpleNamespace(GetActiveCamera=lambda: camera),
        initialized=False,
    )
    frame = np.zeros((4, 6, 3), dtype=np.uint8)
    frame[0, 0] = (1, 2, 3)

    update_glasses_video_frame(scene, frame)

    assert importer.extent == (0, 5, 0, 3, 0, 0)
    assert importer.components == 3
    assert importer.data[1] == frame.nbytes
    assert np.frombuffer(importer.data[0], dtype=np.uint8).reshape(4, 6, 3)[-1, 0].tolist() == [1, 2, 3]
    assert image_actor.position[2] == -100.0
    assert camera.focal_point == (0.0, 0.0, -1.0)
