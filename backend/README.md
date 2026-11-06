# Nityanand Portfolio API

FastAPI service for portfolio content, admin authentication, project management and media uploads.

## Architecture
- SQLAlchemy models: projects, skills, experience, achievements and editable profile sections.
- SQLite by default; set `DATABASE_URL` to a PostgreSQL DSN for production.
- JWT bearer authentication protects all write and upload endpoints.
- Public read endpoints power the portfolio without exposing admin credentials.

## Local setup
1. Create a virtual environment: `python -m venv .venv`
2. Activate it and install: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`; set unique secrets and an Argon2 admin password hash.
4. Generate a hash with: `python -c "from pwdlib import PasswordHash; print(PasswordHash.recommended().hash('YOUR-STRONG-PASSWORD'))"`
5. Start: `uvicorn app.main:app --reload`
6. API docs: `http://127.0.0.1:8000/docs`

Never commit `.env`, real passwords, JWT secrets or uploaded private documents.

## API
- `GET /health`
- Public: `GET /api/v1/projects`, `GET /api/v1/projects/{slug}`, `GET /api/v1/skills`, `GET /api/v1/experience`, `GET /api/v1/achievements`, `GET /api/v1/profile/{key}`
- Auth: `POST /api/v1/auth/login`
- Admin CRUD: `/api/v1/admin/projects`, `skills`, `experience`, `achievements`, `profile/{key}`
- Upload: `POST /api/v1/admin/uploads`

This API is a backend foundation. Configure a persistent-volume host and HTTPS before production; GitHub Pages cannot host FastAPI or SQLite.
