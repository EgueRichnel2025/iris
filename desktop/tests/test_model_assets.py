from pathlib import Path

from iris.vision.model_assets import face_landmarker_model_path


def test_model_path_resolves_from_desktop_source_tree():
    path = face_landmarker_model_path()

    assert path == (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "models"
        / "face_landmarker.task"
    )


def test_model_path_resolves_from_pyinstaller_bundle(monkeypatch, tmp_path):
    monkeypatch.setattr("sys._MEIPASS", str(tmp_path), raising=False)

    assert face_landmarker_model_path() == (
        tmp_path / "assets" / "models" / "face_landmarker.task"
    )
