# Contributing

Thanks for helping improve Corni! Before you start, read the Repository Guidelines for project structure, commands, and conventions: see AGENTS.md.

## Quick Start
- Backend
  - python -m venv .venv && source .venv/bin/activate
  - pip install -r backend/requirements.txt
  - python backend/manage.py migrate && python backend/manage.py runserver
- Frontend
  - cd frontend && npm ci && npm run dev

## Commits and Pull Requests
- Use concise, imperative commit messages (e.g., "Add movie search endpoint").
- Open a PR with: scope summary, linked issue, screenshots/GIFs for UI, and test notes.
- Verify locally: python backend/manage.py test and tsc (implicit via build). For frontend: npm run build if relevant.

## Tests
- Add/extend Django tests near the changed app (e.g., backend/users/tests.py).
- Mock external HTTP calls with unittest.mock.patch.

Questions? Open an issue with steps to reproduce or the intended change.
