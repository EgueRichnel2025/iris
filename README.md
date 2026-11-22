# IRIS

**See beyond yourself.**

IRIS is a local desktop camera application for real-time visual filters and facial effects. It is designed to be launched directly on a computer for live demonstrations.

The camera feed is processed on the device. No account, web service, cloud upload or internet connection is required for the camera experience.

## Current application

The active application lives in [desktop/](desktop/).

- Python 3.12+
- PySide6 desktop interface
- OpenCV camera capture and image processing
- MediaPipe dependency reserved for the upcoming face-tracking layer
- Local photo capture

## Run IRIS

Install [uv](https://docs.astral.sh/uv/) and Python 3.12+, then run:

```bash
cd desktop
uv sync --extra dev
uv run iris
```

## Validate

```bash
cd desktop
uv run pytest
```

## Product direction

IRIS is intentionally a small, camera-first desktop experience:

1. Launch the application.
2. See the live camera preview.
3. Select a visual effect.
4. Capture a photo or record a video.
5. Build a standalone executable for demonstrations.

Core effects planned for the face engine include accessories, expression-reactive filters, mouth deformations and head/face deformations.

The former React web experiment is no longer the active product. Its history is preserved in Git.

## Development notes

See [desktop/README.md](desktop/README.md) and [docs/development/DEVELOPMENT_LOG.md](docs/development/DEVELOPMENT_LOG.md).
