# IRIS — Frontend Visual Direction

**Status:** Proposed design direction for the first UI/UX prototype  
**Brand:** IRIS  
**Tagline:** See beyond yourself.

## 1. Art direction

IRIS should feel like a premium creative camera and social experience: expressive, bright enough to feel playful, but not childish. Avoid the generic AI-product look: no neon purple/blue gradients, no excessive glassmorphism, no glowing borders everywhere and no dashboard-heavy layout.

Use a warm editorial neutral foundation with a vivid iris-inspired accent. The camera preview is the hero; UI chrome should stay quiet and let faces and effects stand out.

## 2. Proposed color palette

| Token | Hex | Intended use |
|---|---|---|
| iris-ink | #202321 | Main text, dark controls |
| iris-paper | #F7F5F0 | Main light background |
| iris-white | #FFFFFF | Cards and surfaces |
| iris-muted | #85877F | Secondary text |
| iris-line | #E7E4DC | Borders and dividers |
| iris-violet | #7357D9 | Primary brand accent, active states |
| iris-violet-soft | #EEE9FF | Selected backgrounds and chips |
| iris-coral | #F27E70 | Playful secondary accent and badges |
| iris-lime | #C7E56B | Small highlights and success accents |
| iris-camera-bg | #171817 | Camera Studio background |
| iris-overlay | #292B29 | Dark Studio panels |

### Color usage rules
- Use paper/white/ink as the dominant product palette.
- Use violet as the recognizable IRIS accent, not as a full-page gradient.
- Coral and lime are supporting accents; use sparingly.
- In Camera Studio, use dark camera surfaces so the live image is dominant.
- Effects and captured content should supply most of the visual color.
- Keep text contrast accessible. Never put small white text on lime.

## 3. Typography

Suggested pairing:
- Headings: DM Sans or Manrope.
- Body and UI: Inter or DM Sans.
- Use strong hierarchy and concise labels.
- Avoid overly thin font weights for controls.

## 4. Main navigation

Primary destinations:
- Explore
- Studio
- My creations
- Profile

Desktop: slim top navigation. Mobile: compact bottom navigation with icons and labels. Studio should be visually prominent.

## 5. Screen layouts

### A. Landing / Explore

Desktop:
- Top bar: IRIS wordmark left; Explore, Studio and My creations in the center/right; Sign in or avatar at far right.
- Hero: large editorial headline on the left (“A new angle on you.”), short copy, primary Open Studio CTA and secondary Explore effects CTA.
- Right: large portrait/camera-inspired visual showing a person with a playful AR effect. This is a design preview, not a live camera.
- Below: horizontal category chips (Trending, Funny, Beauty, Animals, Distortion, 3D).
- Featured filters: image-led cards with preview, name and creator.
- Footer: concise brand statement and links.

Mobile:
- Wordmark and compact menu at top.
- Hero text first, large preview card below.
- Full-width Open Studio button.
- Horizontally scrollable category chips.
- Two-column filter card grid.
- Bottom navigation.

### B. Camera Studio — primary experience

Desktop:
- Full-height dark workspace within the app shell.
- Top row: back/close, IRIS Studio label, camera status and settings.
- Center: large 4:5 or 3:4 live preview with rounded corners. Preview dominates.
- Side utility rail: selected filter, category, intensity slider where relevant, flip camera and timer.
- Capture controls: shutter centered; Photo/Video mode switch; recent capture thumbnail; camera switch.
- Filter tray below preview: horizontally scrollable thumbnails with labels.
- Keep secondary controls subdued.

Mobile:
- Studio uses nearly the full available screen.
- Top row: close/back, IRIS, camera switch.
- Preview takes most of the screen with safe-area spacing.
- Filter tray near the bottom with horizontal scrolling.
- Large shutter button centered; Photo / Video mode selector.
- Effect intensity can open in a bottom sheet.
- Do not permanently cover eyes, mouth or key face areas with controls.
- Touch targets should be comfortably tappable.

### C. Filter detail / selection
- Large preview thumbnail.
- Filter name, short description and creator where applicable.
- Try it action opens Studio with that filter selected.
- Save/favourite action for signed-in users.
- Related filters below.

### D. Capture result
- Large media preview.
- Clear actions: Retake, Download, Share.
- Optional caption only if publishing is selected.
- Explicit privacy/visibility choice before any server upload.
- Never auto-publish.

### E. My creations (later)
- Grid of private captures and saved filters.
- Tabs for Captures, Saved filters and My filters.
- Empty state inviting the user to open Studio.

## 6. Reusable components

- AppHeader
- DesktopNavigation
- MobileBottomNavigation
- PrimaryButton / SecondaryButton
- CategoryChip
- FilterCard
- FilterTray
- CameraPreview
- CameraStatus
- CaptureControls
- ModeSwitcher
- EffectIntensityControl
- PermissionDialog
- CaptureResultPanel
- EmptyState
- Toast / InlineNotice

## 7. Interaction and motion

- Subtle transitions (150–220 ms) for menus, tabs and selection.
- Filter selection should feel immediate.
- Use restrained scale/opacity transitions for selected filter cards.
- Avoid motion that competes with face tracking.
- Respect reduced-motion preferences.
- Show a clear model-loading indicator before effects become available.
- Provide visible camera permission and camera unavailable states.

## 8. Responsive behavior

- Mobile-first, tested at 320px, 375px, 390px and 430px widths.
- Tablet layout preserves camera prominence.
- Desktop Explore content has a readable maximum width; Studio can use a wider workspace.
- No horizontal page overflow.
- Studio controls remain reachable without obscuring the face.

## 9. Design prototype acceptance criteria

- Landing communicates the product within seconds.
- Open Studio is the most prominent action.
- Studio makes the camera preview the visual focus.
- Filter tray is easy to browse on touch devices.
- Capture action is obvious and reachable.
- Palette feels creative and premium, not like a generic AI dashboard.
- Desktop and mobile layouts are intentionally designed.
- Include representative states: landing, camera permission prompt, live Studio with a selected filter, and capture result.

## 10. Implementation notes

A static prototype can use carefully chosen placeholder images and mock filter thumbnails. It must not request real camera access. Actual camera integration belongs to the Camera Integration phase.
