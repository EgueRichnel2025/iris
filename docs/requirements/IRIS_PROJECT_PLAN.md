# IRIS — Project Plan & Product Requirements

**Tagline:** See beyond yourself.  
**Product:** Browser-based real-time camera effects, Computer Vision, Augmented Reality and creative sharing.  
**Status:** Planning  
**Repository:** https://github.com/EgueRichnel2025/iris

## 1. Vision

IRIS is a web creative-camera platform. Users open it on a phone or computer, grant camera access, explore live face filters and distortions, capture photos or videos, and share creations. The longer-term vision includes a community filter library and a creator tool for custom effects.

IRIS must feel like a polished creative product, not a technical demo. Basic camera experimentation should eventually be possible without creating an account.

## 2. Product principles

- Camera-first: the live preview and selected effect are the primary focus in Studio.
- Local processing: face analysis and effects run in the browser wherever practical.
- Privacy by design: camera frames are not uploaded by default; ask explicitly before uploading or publishing captured media.
- Mobile-first: prioritize touch interaction and responsive layouts.
- Performance: stable tracking and graceful fallback on weaker devices.
- Accessibility: readable contrast, clear permission and error states, keyboard support where relevant.
- Modular engineering: separate vision, deformation, filters, rendering, capture and social features.
- No fake functionality: unfinished features must be excluded or clearly marked.

## 3. Users and core journeys

### Target users
- People who want to have fun with camera filters and share content with friends.
- Creators experimenting with visual effects.
- Future community creators publishing reusable filters.

### Journey A — Try a filter
1. Open IRIS.
2. Select Open Studio.
3. Read the camera-use notice and grant browser permission.
4. See the live camera preview.
5. Choose an effect from the filter tray.
6. Move the head and make expressions; the effect follows.
7. Switch or remove the effect.

### Journey B — Capture and share
1. Select a filter.
2. Capture a photo or record a short video.
3. Preview the result.
4. Retake, download or use the native share sheet when supported.
5. If publishing is enabled, explicitly choose visibility and confirm upload.

### Journey C — Discover filters
1. Browse featured effects and categories.
2. Preview a filter card.
3. Open it in Studio.
4. Save it to favourites when signed in (later account feature).

## 4. Functional scope

### 4.1 Camera Studio
- Request camera permission through the browser.
- Start and stop camera streams cleanly.
- Switch front/rear cameras when available.
- Show loading, denied, unavailable and device-in-use states.
- Support responsive preview aspect ratios.
- Select and clear filters without restarting the camera.
- Capture still images.
- Record video with the rendered effect where supported.
- Provide retake, download and native share actions where supported.
- Stop media tracks when leaving Studio.

### 4.2 Face Vision Engine
- Real-time face detection and landmark tracking.
- Facial landmark positions and transformation data.
- Expression signals / blendshape scores where available.
- Handle no-face, multiple-face and tracking-loss states.
- Smooth jitter without introducing excessive lag.
- Keep the vision provider behind an abstraction.

### 4.3 2D Filter Engine
- Position, scale and rotate transparent assets using facial landmarks.
- Support anchor points, offsets, scale rules and rotation rules.
- Support layered assets and draw ordering.
- Support simple animation and expression-triggered visibility.
- Define filter metadata: identifier, name, category, thumbnail, assets, anchors, capabilities and version.

### 4.4 Facial Deformation Engine — core feature
Deformations are a first-class IRIS feature.

**Mouth and lips**
- Enlarge or shrink the mouth.
- Widen or narrow the mouth.
- Stretch horizontally or vertically.
- Exaggerate lips and create comic expressions.
- Trigger selected deformations from mouth opening or expression signals.

**Head and face**
- Big Head / Small Head.
- Widen or narrow the face.
- Squash / stretch.
- Exaggerate cheeks and selected facial regions.
- Keep deformations attached during head rotation and movement.

**Technical direction**
- Start with controlled 2D mesh warping driven by facial landmarks.
- Investigate triangulated facial meshes and local geometric transformations.
- Evaluate GPU shaders / WebGL for demanding effects.
- Avoid naive whole-frame scaling that distorts the background.
- Define safeguards for extreme parameters, edge artifacts and tracking loss.
- Validate across face shapes, lighting conditions and camera angles.

### 4.5 Intelligent and animated effects
- Smile-triggered effects.
- Mouth-open-triggered effects.
- Blink-triggered effects.
- Head-pose-triggered effects.
- Animated overlays anchored to facial landmarks.
- Sensitivity thresholds and smoothing to prevent flicker.

### 4.6 3D AR Engine
- Render 3D masks and accessories.
- Attach objects to face pose / transformation.
- Support lighting and material configuration.
- Evaluate occlusion and depth handling.
- Stage 3D after a reliable 2D engine.

### 4.7 Photo and video
- Capture the composited output, not only the raw camera frame.
- Preview and retake.
- Download media.
- Add text and stickers in a later editor iteration.
- Export using browser-supported formats and communicate limitations.

### 4.8 Accounts and personal library
- Optional account creation and sign-in.
- User profile.
- Saved filters and favourites.
- Personal creation library.
- Account and privacy settings.

### 4.9 Community and sharing
- Public filter discovery.
- Publish user-created filters after moderation controls exist.
- Likes, follows and creator profiles as later features.
- Share links to published creations.
- Native share sheet and downloads for the initial release.
- Reporting and moderation workflows before opening public user-generated content.

### 4.10 Filter Creator
- Create filters from approved templates.
- Upload transparent image assets.
- Configure anchors, scale and offsets.
- Preview against live face tracking.
- Save drafts and publish after validation.
- Consider advanced 3D authoring later.

## 5. Proposed technology direction

Choices are provisional until validated with technical spikes.

| Area | Initial direction |
|---|---|
| Frontend | React + TypeScript + Vite |
| Styling | Tailwind CSS and design tokens |
| Face tracking | MediaPipe Face Landmarker |
| Image processing | Canvas API; OpenCV.js only where useful |
| 2D rendering | Canvas 2D, with an abstraction for future GPU rendering |
| 3D rendering | Three.js / WebGL |
| Backend | Node.js API only where custom server logic is needed |
| Data | PostgreSQL |
| Authentication / storage | Evaluate Supabase |
| Tests | Vitest, React Testing Library, Playwright |
| Quality | ESLint, Prettier, TypeScript strict mode |

Do not introduce a backend to process camera frames. Real-time face analysis should run client-side by default. Backend services are for accounts, metadata, user libraries, moderation and explicitly requested uploads.

## 6. Architecture boundaries

Suggested monorepo:
- apps/web: browser application and user experience.
- apps/api: optional API for accounts, filter catalogue and community.
- packages/vision-engine: face landmark and expression abstraction.
- packages/filter-engine: filter definitions, anchors and orchestration.
- packages/deformation-engine: mesh construction and facial warping.
- packages/rendering-engine: canvas and 3D rendering adapters.
- packages/shared: shared types, schemas and utilities.
- docs: product, architecture, design and development documentation.

Keep the vision provider behind an interface so UI components do not depend directly on a specific MediaPipe implementation.

## 7. Development roadmap — 16 phases

### Phase 01 — Product Foundation
Goal: confirm scope, requirements, user journeys and constraints.  
Deliverables: this plan, glossary, scope and acceptance criteria.  
Exit: core journeys and MVP scope are documented.

### Phase 02 — Project Setup
Goal: establish a maintainable monorepo and workflow.  
Deliverables: workspace configuration, TypeScript, linting, formatting, tests, environment conventions and initial CI.  
Exit: clean install, lint, typecheck and tests succeed.

### Phase 03 — UI/UX Foundation
Goal: implement the visual system and responsive application shell.  
Deliverables: design tokens, typography, navigation, landing page, Studio shell, reusable controls and responsive states.  
Exit: key screens render consistently on mobile and desktop.

### Phase 04 — Camera Integration
Goal: provide reliable camera access.  
Deliverables: camera service, permission handling, device switching, loading/error states and lifecycle cleanup.  
Exit: camera starts, switches and stops reliably on supported browsers.

### Phase 05 — Computer Vision Core
Goal: integrate face landmark inference in the browser.  
Deliverables: vision adapter, model loading, inference loop and typed face result.  
Exit: landmarks are available from live frames without sending frames to a server.

### Phase 06 — Face Tracking
Goal: stabilize tracking and expression signals.  
Deliverables: smoothing, pose data, blendshape adapter, tracking state and performance instrumentation.  
Exit: tracking remains usable during ordinary movement and recovers after temporary loss.

### Phase 07 — 2D Filter Engine
Goal: render anchored 2D effects.  
Deliverables: filter schema, anchor system, asset loader, layering and initial filter pack.  
Exit: several filters follow face position, scale and rotation.

### Phase 08 — Facial Deformation Engine
Goal: implement mouth and head distortions as core effects.  
Deliverables: facial mesh, mouth warp operators, head/face warp operators, parameter controls and regression samples.  
Exit: deformations work in real time, remain localized to the face and recover gracefully after tracking loss.

### Phase 09 — Intelligent Effects
Goal: connect effects to expressions and actions.  
Deliverables: trigger rules, thresholds, cooldowns and animation controller.  
Exit: smile, blink and mouth-open effects trigger reliably without excessive flicker.

### Phase 10 — 3D AR Engine
Goal: introduce 3D face-attached objects and masks.  
Deliverables: Three.js renderer, face pose attachment, materials and initial 3D effects.  
Exit: selected 3D assets remain aligned during head movement on supported devices.

### Phase 11 — Photo and Video
Goal: capture the final composited output.  
Deliverables: photo capture, video recording, preview, retake, download and export error handling.  
Exit: exported media contains the selected effect and plays outside the app.

### Phase 12 — Accounts and Personal Library
Goal: add optional identity and saved content.  
Deliverables: authentication, profile, favourites and private library.  
Exit: users can manage their account and private saved items securely.

### Phase 13 — Filter Discovery and Community
Goal: let users discover and interact with shared filters.  
Deliverables: catalogue, categories, creator pages, likes, follows, reporting and moderation foundations.  
Exit: published content has visibility controls and abuse-reporting paths.

### Phase 14 — Filter Creator
Goal: let users create reusable filters.  
Deliverables: asset import, anchor editor, parameter configuration, preview, draft and publish workflow.  
Exit: a user can create and reuse a valid 2D filter without editing source code.

### Phase 15 — Quality, Security and Optimization
Goal: prepare IRIS for real users.  
Deliverables: automated tests, browser/device matrix, performance profiling, accessibility, privacy and security reviews.  
Exit: critical journeys pass and known limitations are documented.

### Phase 16 — Deployment and Release
Goal: publish a stable public application.  
Deliverables: production deployment, domain and HTTPS, monitoring, error reporting, backups and release documentation.  
Exit: users can access IRIS publicly and use supported camera features securely.

## 8. MVP definition

The first public-quality MVP should prioritize:
- Responsive landing page.
- Camera Studio.
- Camera permission and device handling.
- Face landmarks and stable tracking.
- Curated pack of 2D accessory filters.
- Core mouth and head deformation effects.
- A small set of expression-triggered effects.
- Photo capture and short video recording with effects.
- Download and native sharing.
- Clear privacy messaging.

Accounts, public community, creator marketplace and advanced 3D authoring can follow once the camera and effect experience is reliable.

## 9. Non-functional requirements

- Camera processing stays on-device by default.
- No camera access before explicit user permission.
- Stop camera tracks when Studio closes.
- Never publish captured content without explicit user action.
- Responsive layout from small mobile screens to desktop.
- Handle unsupported APIs and weaker devices gracefully.
- Avoid blocking the UI during model loading or inference.
- Monitor frame rate and inference latency.
- Provide clear loading, empty, error and permission-denied states.
- Keep dependencies justified and updated.

## 10. Git workflow

- Target at least one meaningful commit on every active project day.
- Make additional commits whenever independent, validated work is completed.
- Keep commits small and atomic.
- Run relevant tests, linting or type checks before committing.
- Use clear English Conventional Commit messages.
- Push regularly to keep remote history current.
- Never create empty or artificial commits to inflate the count.
- Documentation, tests, refactoring and research spikes are valid commits when they deliver real value.

Suggested format: type(scope): concise description

Examples:
- docs(product): define IRIS scope and user journeys
- chore(tooling): configure TypeScript and linting
- feat(camera): add camera permission state
- test(vision): cover landmark normalization
- feat(deformation): implement mouth width warp

## 11. Initial acceptance demonstration

1. Open IRIS in a supported browser.
2. Grant camera permission.
3. See a live camera preview.
4. Detect a face and visualize facial landmarks.
5. Select a glasses overlay.
6. Turn and tilt the head while the overlay remains attached.
7. Apply a mouth deformation and a head deformation.
8. Capture a photo containing the rendered effect.

This proves the foundation of the IRIS camera and effect pipeline.

## 12. Decisions to validate during implementation

- Exact browser and mobile support matrix.
- MediaPipe model configuration and performance targets.
- Whether deformation rendering should remain Canvas-based or move to WebGL shaders.
- Backend framework and hosting provider.
- Storage provider, retention policy and media size limits.
- Community moderation and publication rules.
- Final brand assets, domain and trademark availability.

Record decisions when validated; do not silently treat provisional choices as final.
