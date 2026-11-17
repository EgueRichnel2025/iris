# IRIS authentication setup

IRIS uses Supabase Auth for email/password registration, sign-in and password-reset emails.

## Local configuration

1. Create a Supabase project.
2. Open the project's Connect / API settings and copy the project URL and publishable (or legacy anon) key.
3. Copy `apps/web/.env.example` to `apps/web/.env.local`.
4. Set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` in `.env.local`.
5. Restart the Vite development server.
6. In Supabase Authentication settings, configure the site URL and add the local development URL (for example `http://localhost:5173`) to the allowed redirect URLs.
7. Configure the email provider / SMTP before testing confirmation and password recovery emails.

Never put a Supabase service-role key in a Vite environment variable or commit `.env.local`. Only the public publishable/anon key belongs in the browser.

## Current behavior

- Sign up creates an auth user and stores the supplied display name in user metadata.
- If email confirmation is enabled, the user must confirm the email before signing in.
- Sign in uses Supabase email/password authentication.
- Password recovery requests a reset email.
- If the environment variables are absent, the UI displays an actionable configuration error rather than pretending that an account was created.

The Explore dashboard is still accessible in preview mode. Profile persistence and protected routes will be implemented in a later authentication milestone.
