# IRIS — Supabase project configuration

## Provisioned project

- Project: `iris`
- Project ref: `dvsdqwtklqvxahmkgwln`
- Region: `eu-west-1` (Ireland)
- Project status at setup: `ACTIVE_HEALTHY`
- API URL: stored in `apps/web/.env.local`
- Browser key: Supabase publishable key, stored in `apps/web/.env.local`

The local environment file is ignored by Git. Never commit it, and never use a Supabase secret/service-role key in the browser.

## Authentication settings observed

The Auth settings endpoint currently reports:

- Email/password provider enabled.
- New signups enabled.
- Email confirmation required (`mailer_autoconfirm=false`).
- Google OAuth disabled.
- No application tables exist yet in the public schema.

IRIS currently implements email/password sign-up, sign-in, password recovery, persisted sessions, and restoration of the session when the app starts. The display name is stored in Auth user metadata (`full_name`).

## Required dashboard settings before testing confirmation emails

Open the Supabase project dashboard:

1. Authentication → URL Configuration.
2. Set Site URL to `http://localhost:5173` for local development.
3. Add `http://localhost:5173/**` to the allowed Redirect URLs.
4. For a deployed app, add its HTTPS origin separately and use that origin as the production Site URL.
5. Authentication → SMTP Settings: configure a trusted custom SMTP provider before expecting reliable confirmation and password-reset emails to arbitrary addresses. The built-in email service is restricted for production use.

Google sign-in is intentionally not shown in IRIS yet because the Google provider is disabled and no OAuth client credentials have been configured.

## Local development

The credentials have already been written to `apps/web/.env.local`. Restart Vite after changing environment variables:

```bash
npm run dev --workspace @iris/web -- --host 0.0.0.0
```

The Vite server was restarted after the local environment was added.

## Validation

- Supabase project status: healthy.
- Auth settings endpoint: reachable; email provider enabled; signups enabled.
- Public schema: no tables yet (expected for the current Auth-only milestone).
- Automated tests: 13 passing.
- Lint: clean.
- TypeScript: clean.
- Production build: successful; existing large-bundle warning remains due to MediaPipe.
