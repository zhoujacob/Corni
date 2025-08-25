# Repository Guidelines

## Project Structure & Module Organization
- Backend: Django project in `backend/` with apps `users/` and `movies/`. Settings are split under `backend/corni_backend/settings/` (`local.py` default via `DJANGO_ENV`, `production.py` for deploy). SQLite DB at `backend/db.sqlite3` for local use.
- Frontend: React + TypeScript via Vite in `frontend/`. Source in `frontend/src/` with feature folders (`api/`, `features/`, `pages/`, `shared/`, `types/`). Build output in `frontend/dist/`.
- Tests: Backend tests live beside apps (e.g., `backend/users/tests.py`, `backend/movies/tests.py`). No frontend test runner configured yet.

## Build, Test, and Development Commands
- Backend setup: `python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt`
- Migrate DB: `python backend/manage.py migrate`
- Run API (local): `python backend/manage.py runserver` (serves at `http://localhost:8000`, docs at `/api/docs`)
- Backend tests: `python backend/manage.py test`
- Frontend install: `cd frontend && npm ci`
- Frontend dev: `npm run dev` (Vite at `http://localhost:5173`)
- Frontend build/preview: `npm run build && npm run preview`

## Coding Style & Naming Conventions
- Python: Follow PEP 8, 4‑space indents, snake_case for functions/vars, PascalCase for models/serializers/views. Keep app boundaries clear (`users` vs `movies`).
- TypeScript/React: Strict TS is enabled (`tsconfig.json`). Use PascalCase for components (`DashboardCard.tsx`), camelCase for props/state, co-locate CSS Modules as `Component.module.css`.
- Imports: Prefer absolute aliases in frontend via `@/` (configured in `vite.config.ts`).

## Testing Guidelines
- Framework: Django test runner + DRF `APITestCase` (see `backend/users/tests.py`).
- Conventions: Name tests `test_*` and group by view/serializer behavior. Mock external HTTP calls with `unittest.mock.patch`.
- Running: `python backend/manage.py test` from repo root. Aim to cover new endpoints and permission logic.

## Commit & Pull Request Guidelines
- Commits: Use concise, imperative messages (e.g., "Add movie search endpoint"). Group related changes; avoid noisy formatting-only commits mixed with logic.
- PRs: Include scope summary, linked issue (if any), screenshots/GIFs for UI changes, and test notes (how to reproduce, commands). Ensure `tsc` passes and backend tests are green.

## Security & Configuration Tips
- Backend secrets via `python-decouple`: set `DJANGO_SECRET_KEY`, `GOOGLE_SSO_*`, `TMDB_*` (e.g., in `backend/.env` or environment). Never commit secrets.
- CORS: Local origin allowed at `http://localhost:5173`. Frontend base URL via `frontend/.env*` (`VITE_API_BASE_URL`).
