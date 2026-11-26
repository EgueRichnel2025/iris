<div align="center">

# IRIS

### See beyond yourself.

A local desktop camera application for real-time visual filters and facial effects.

![Status](https://img.shields.io/badge/status-active_development-7357D9?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-desktop-202321?style=for-the-badge)
![Privacy](https://img.shields.io/badge/processing-local-477B42?style=for-the-badge)

</div>

---

## Overview

IRIS turns a computer camera into a live visual-effects studio. Choose an image effect, see the result instantly, and capture photos without sending camera frames to a cloud service.

The active product is the **native desktop application** in `desktop/`. It runs locally and does not require an account or an internet connection for its camera experience.

## Current features

| Feature | Status |
| --- | --- |
| Live webcam preview | Available |
| Real-time image filters — Original, Warm, Cool, Noir, Vivid and Soft Focus | Available |
| Camera controls and FPS display | Available |
| Local photo capture | Available |
| Face landmarks and tracking | Planned |
| Face accessories and AR overlays | Planned |
| Mouth and face deformations | Planned |
| Video recording | Planned |

## Technology stack

The stack is grouped by responsibility. The first groups describe the active desktop application; planned and archived technologies are identified separately.

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Desktop application</h3>
      <p>Application runtime and native user interface.</p>
      <p>
        <img alt="Python" src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white">
        <img alt="PySide6" src="https://img.shields.io/badge/PySide6-Desktop_UI-41CD52?logo=qt&logoColor=white">
      </p>
    </td>
    <td width="50%" valign="top">
      <h3>Computer vision & camera</h3>
      <p>Camera acquisition and the future facial-analysis layer.</p>
      <p>
        <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-Camera_%26_Vision-5C3EE8?logo=opencv&logoColor=white">
        <img alt="MediaPipe" src="https://img.shields.io/badge/MediaPipe-Face_tracking_planned-4285F4?logo=google&logoColor=white">
      </p>
      <small>MediaPipe is declared as a dependency; its integration into the active desktop frame pipeline is still planned.</small>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Image processing</h3>
      <p>Pixel-level operations and real-time visual effects.</p>
      <p>
        <img alt="NumPy" src="https://img.shields.io/badge/NumPy-Array_processing-013243?logo=numpy&logoColor=white">
        <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-Image_processing-5C3EE8?logo=opencv&logoColor=white">
      </p>
    </td>
    <td width="50%" valign="top">
      <h3>Build & distribution</h3>
      <p>Packaging the desktop application as a standalone executable.</p>
      <p>
        <img alt="PyInstaller" src="https://img.shields.io/badge/PyInstaller-Application_packaging-eeeeee?logo=python&logoColor=3776AB">
      </p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Development & quality</h3>
      <p>Dependency management, automated tests and continuous integration.</p>
      <p>
        <img alt="uv" src="https://img.shields.io/badge/uv-Project_management-DE5FE9">
        <img alt="pytest" src="https://img.shields.io/badge/pytest-Testing-0A9EDC?logo=pytest&logoColor=white">
        <img alt="GitHub Actions" src="https://img.shields.io/badge/GitHub_Actions-CI-2088FF?logo=githubactions&logoColor=white">
      </p>
    </td>
    <td width="50%" valign="top">
      <h3>Archived web experiment</h3>
      <p>The former browser-based prototype is retained in `legacy/web/`; it is not part of the active desktop runtime.</p>
      <p>
        <img alt="React" src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=20232A">
        <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-7-3178C6?logo=typescript&logoColor=white">
        <img alt="Vite" src="https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white">
        <img alt="Supabase" src="https://img.shields.io/badge/Supabase-Prototype-3FCF8E?logo=supabase&logoColor=white">
      </p>
    </td>
  </tr>
</table>

## How it works

```text
Webcam
  │
  ▼
OpenCV camera acquisition
  │
  ▼
Frame processing (OpenCV + NumPy)
  │
  ▼
PySide6 desktop interface
  │
  ├── Live preview
  └── Local photo capture
```

The camera runs in a dedicated thread so that frame acquisition does not block the interface. Each frame is processed locally before being displayed.

## Getting started

### Requirements

- Python 3.12 or newer (below 3.15)
- [uv](https://docs.astral.sh/uv/)
- A working webcam

### Install and launch

From the repository root:

```bash
cd desktop
uv sync --extra dev
uv run iris
```

### Run the tests

```bash
cd desktop
uv run pytest
```

## Build a standalone application

Build scripts are provided for Linux and Windows.

**Linux**
```bash
cd desktop
./build.sh
```

**Windows PowerShell**
```powershell
cd desktop
.\build.ps1
```

PyInstaller creates a build for the operating system on which the command is run. The currently validated bundle is the Linux build.

## Project structure

```text
iris/
├── desktop/                 # Active Python desktop application
│   ├── iris/                # Camera, effects and interface
│   ├── tests/               # Desktop tests
│   ├── pyproject.toml       # Python dependencies and tooling
│   ├── build.sh             # Linux packaging
│   └── build.ps1            # Windows packaging
├── docs/
│   ├── development/         # Development notes and setup
│   └── requirements/        # Product and technical plans
├── legacy/
│   └── web/                 # Archived React web experiment
└── .github/
    └── workflows/           # Continuous integration
```

## Roadmap

1. Strengthen the desktop camera and rendering foundation.
2. Integrate face detection, facial landmarks and stable tracking.
3. Add face accessories and AR overlays.
4. Implement mesh-based mouth and face deformations.
5. Add expression-driven effects and video capture.
6. Improve performance and cross-platform distribution.

## Documentation

- [Desktop application guide](desktop/README.md)
- [Desktop implementation plan](docs/requirements/IRIS_DESKTOP_PLAN.md)
- [Project plan](docs/requirements/IRIS_PROJECT_PLAN.md)
- [Development log](docs/development/DEVELOPMENT_LOG.md)

---

<div align="center">
  <sub>IRIS — See beyond yourself.</sub>
</div>
