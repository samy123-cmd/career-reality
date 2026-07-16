# AGENTS.md

## Cursor Cloud specific instructions

This is a **Django 6** project ("Career Reality", an Indian tech career/salary site). It is a single web
service. Python 3.12 is required.

### Environment / running locally

- Dependencies live in `requirements.txt` and are installed into a virtualenv at `.venv` (created by the
  startup update script). Activate it with `. .venv/bin/activate` before running any command.
- Local development uses **SQLite** and an **in-memory cache** automatically: when `DATABASE_URL` /
  `POSTGRES_URL` and `REDIS_URL` are unset, `config/settings.py` falls back to `db.sqlite3` and locmem.
  No Postgres/Redis is needed for local dev or tests.
- You MUST run with `DEBUG=True` locally. When `DEBUG=False`, `SECRET_KEY` and `ALLOWED_HOSTS` are
  required and the app raises at startup. Convenience env for commands:
  `export DEBUG=True SECRET_KEY=local-dev-only`.
- `scripts/manage.sh <cmd>` is a helper that sources `.env` (if present) and defaults `DEBUG=True` +
  a dev `SECRET_KEY`, then runs `python3 manage.py <cmd>`. Note it calls system `python3`, so activate
  `.venv` first (or use `.venv/bin/python manage.py ...` directly).
- `db.sqlite3` is gitignored, so on a fresh machine run migrations before starting the server:
  `python manage.py migrate`. The dev DB starts empty (no seeded articles/companies/salary data).

### Run / test / build commands

- Run dev server: `python manage.py runserver 0.0.0.0:8000` (with `DEBUG=True SECRET_KEY=...`).
- Lint / validate: there is **no separate linter** (no flake8/ruff/pylint config). Use
  `python manage.py check` as the validation step.
- Tests: `python manage.py test` (Django test runner; ~247 tests, runs on an in-memory SQLite DB).
- Build (production only, not needed for dev): `build_files.sh` runs `migrate` + `collectstatic`.
  Deployment target is Vercel (`api/index.py` WSGI entrypoint, `vercel.json`).

### Known gotchas

- A handful of tests (currently ~4, e.g. `core.test_seo_p2.LandingPageSEOTests` and `search.tests`)
  assert on specific seeded/pillar content that does not exist in a fresh test DB. These are
  pre-existing content-dependent failures, not environment problems — the app itself runs fine.
- All third-party API keys (Razorpay, Resend, OpenAI, Google OAuth) are optional and degrade
  gracefully when unset; they are only required to exercise payments / email / AI / social-login flows.
