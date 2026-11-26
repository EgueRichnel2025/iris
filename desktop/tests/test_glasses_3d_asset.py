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
