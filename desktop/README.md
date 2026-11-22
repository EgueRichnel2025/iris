# IRIS Desktop

IRIS is a local desktop camera application for real-time visual filters and face effects.

## Current MVP

- Desktop interface built with PySide6.
- Live camera preview powered by OpenCV.
- Local image effects: Original, Warm, Cool, Noir, Vivid and Soft Focus.
- Photo capture saved to the user's Pictures/IRIS folder.
- Camera processing stays on the device.

## Run from source

From the repository root:

```bash
cd desktop
uv sync --extra dev
uv run iris
```

Alternatively, after activating the environment:

```bash
python -m iris
```

## Checks

```bash
uv run pytest
```

## Build a standalone application

On Linux:

```bash
./build.sh
```

On Windows PowerShell:

```powershell
.\build.ps1
```

PyInstaller builds for the operating system on which it runs. Run the PowerShell script on Windows to produce the Windows executable.
