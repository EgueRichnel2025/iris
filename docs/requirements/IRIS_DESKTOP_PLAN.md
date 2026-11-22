# IRIS Desktop — Product & Engineering Plan

## Product definition

IRIS is a small, local desktop camera application for live demonstrations. It is not a website, social network or cloud service.

The user launches the application, sees a live webcam preview, selects an effect and captures a photo or video. Camera frames and effects are processed locally.

## Product principles

- Desktop-first, camera-first, minimal interaction.
- No sign-in, user profile, feed, backend or cloud media storage.
- Camera access begins when the application launches and can be stopped by the user.
- Camera frames are processed locally and are never uploaded.
- Effects must remain visually stable while the user moves.
- The application must be distributable as a standalone executable.

## Target architecture

| Layer | Technology | Responsibility |
|---|---|---|
| Desktop UI | PySide6 | Window, controls, effect picker, capture feedback |
| Camera | OpenCV | Webcam access, frame acquisition, photo/video capture |
| Face tracking | MediaPipe Face Landmarker | Face landmarks, blendshapes, pose |
| Image processing | NumPy + OpenCV | 2D overlays, masks and geometric warps |
| 3D effects (later) | OpenGL / Qt rendering | Anchored 3D accessories |
| Packaging | PyInstaller | Standalone desktop executable |

## Delivery roadmap

### Phase 1 — Desktop foundation
- Native window and camera preview.
- Camera lifecycle and error states.
- Basic local color effects.
- Photo capture.
- Unit tests for image effects.

### Phase 2 — Face tracking
- MediaPipe model lifecycle and local model assets.
- Face landmarks and blendshape signals.
- Stable tracking, smoothing and performance metrics.

### Phase 3 — 2D AR effects
- Glasses, hats, crowns and animal ears.
- Face-anchored positioning, scale and rotation.
- Effect catalog and preview thumbnails.

### Phase 4 — Facial deformations
- Mouth widen, shrink, enlarge and stretch.
- Big head, small head, widen, narrow and squash/stretch.
- Stable mesh warping with minimal edge artifacts.

### Phase 5 — Expression-reactive effects
- Mouth-open triggers, smile, blink and head movement.
- Configurable thresholds and smoothing.

### Phase 6 — Capture and distribution
- Video recording with rendered effects.
- Local media gallery.
- Performance profiling and camera compatibility.
- Windows executable build and clean-machine smoke test.

## Definition of the first demonstration

1. Launch IRIS as a desktop application.
2. See the webcam preview without a browser.
3. Switch between multiple visual effects.
4. See a selected effect update the live preview.
5. Capture a photo locally.
6. Close IRIS and confirm the camera is released.

## Development workflow

- Small, atomic and validated commits.
- At least one meaningful commit on every day of project work.
- Unit tests for deterministic image processing.
- Manual webcam validation for camera behavior.
- Keep the development log current.
