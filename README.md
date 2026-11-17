# IRIS

**See beyond yourself.**

IRIS is a browser-based creative camera focused on real-time computer vision, augmented-reality filters, facial deformations and creative sharing.

## Repository structure

```text
iris/
├── apps/
│   └── web/          # React + TypeScript browser application
├── docs/
│   └── requirements/ # Product requirements and design direction
├── packages/         # Shared engines and reusable packages
└── prototype/        # Approved interactive product prototype
```

## Requirements

- Node.js >= 22.12
- npm >= 10.9

## Development

```bash
npm install
npm run dev
```

## Quality checks

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

## Product principles

- Camera processing runs locally in the browser by default.
- Camera access starts only after explicit user permission.
- Captured media is never uploaded or published without explicit action.
- Mobile-first, accessible and performance-conscious experiences.
- Facial deformations (mouth and head) are core product capabilities.

See [the project plan](docs/requirements/IRIS_PROJECT_PLAN.md) and [the frontend design direction](docs/requirements/IRIS_FRONTEND_DESIGN.md).
