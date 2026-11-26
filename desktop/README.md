# IRIS Desktop

The active native application for real-time camera filters and facial effects.

## Technology stack

| Area | Technologies | Responsibility |
| --- | --- | --- |
| Runtime | Python 3.12+ | Application logic |
| Desktop UI | PySide6 Essentials | Native interface and camera preview |
| Camera & computer vision | OpenCV | Webcam acquisition, frame conversion and image operations |
| Image processing | NumPy, OpenCV | Array operations and visual effects |
| Face analysis | MediaPipe Face Landmarker | 478 facial landmarks, VIDEO-mode tracking and temporal smoothing |
| Packaging | PyInstaller | Standalone application builds |
| Testing | pytest | Automated desktop tests |
| Dependency management | uv | Environment and dependency synchronisation |

## Current features

- Native desktop interface built with PySide6.
- Live camera preview powered by OpenCV.
- Real-time image effects: Original, Warm, Cool, Noir, Vivid and Soft Focus.
- Camera pause and restart controls with an FPS display.
- Local photo capture in the user's `Pictures/IRIS` folder.
- Camera frames are processed on the device.
- Real-time face detection with a 478-point facial landmark overlay.
- Temporal EMA smoothing to reduce landmark jitter.
- Face detection runs in the camera thread; the UI only displays its status.

## Run from source

Requirements: Python 3.12+ (below 3.15) and [uv](https://docs.astral.sh/uv/).

From the repository root:

```bash
cd desktop
uv sync --extra dev
uv run iris
```

To launch the Python module directly:

```bash
uv run --no-sync python -m iris
```

## Run the tests

```bash
uv run pytest
```

## Build a standalone application

**Linux**
```bash
./build.sh
```

**Windows PowerShell**
```powershell
.\build.ps1
```

PyInstaller builds for the operating system on which it runs. Run the PowerShell script on Windows to produce a Windows executable.

### Build output

- Linux: `dist/IRIS/IRIS`
- Windows: `dist/IRIS/IRIS.exe`

A Linux bundle has been generated and smoke-tested. Its current size is larger than the target because this development environment uses a system OpenCV build with many optional native libraries. The Windows PowerShell build script must be run on a Windows machine.

## Related documentation

- [Main project README](../README.md)
- [Desktop implementation plan](../docs/requirements/IRIS_DESKTOP_PLAN.md)
- [Development log](../docs/development/DEVELOPMENT_LOG.md)
