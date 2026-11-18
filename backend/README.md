# Nityanand Portfolio API

Free/open-source FastAPI backend. The recommended zero-cost setup is self-hosted Docker Compose with SQLite; no paid hosting or managed database is required.

## Free self-hosted deployment
- Frontend: GitHub Pages — https://circuittocode.github.io/
- API: FastAPI in Docker on your own always-on computer/server
- Database: SQLite in a persistent Docker volume
- Authentication: JWT + Argon2
- Uploads: persistent local Docker volume

GitHub Pages serves static files only. It cannot run FastAPI or host a persistent database. The API must run separately on an always-on host. Public access requires HTTPS and a secure reverse proxy; do not expose port 8000 directly to the internet.

## Configure secrets
From the repository root:

```powershell
cd backend
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python -c "from pwdlib import PasswordHash; print(PasswordHash.recommended().hash('REPLACE-WITH-YOUR-OWN-PASSWORD'))"
```

Copy `.env.example` to `.env`, then replace `JWT_SECRET` with a long random secret and `ADMIN_PASSWORD_HASH` with the generated Argon2 hash. Never commit `.env`.

## Run with Docker Compose
From the repository root, with Docker installed:

```bash
docker compose up -d --build
docker compose logs -f portfolio-api
```

- Health: http://localhost:8000/health
- API docs: http://localhost:8000/docs

Database and uploads persist in the `portfolio_data` Docker volume. Back it up regularly.

## Run without Docker (development)
From `backend/`:

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

For this local-only mode, set `DATABASE_URL=sqlite:///./portfolio.db` and `UPLOAD_DIR=uploads` in `.env`.

## API routes
- `GET /health`
- Public: `/api/v1/projects`, `/api/v1/projects/{slug}`, `/api/v1/skills`, `/api/v1/experience`, `/api/v1/achievements`, `/api/v1/profile/{key}`
- Login: `POST /api/v1/auth/login`
- Admin CRUD: `/api/v1/admin/projects`, `/skills`, `/experience`, `/achievements`, `/profile/{key}`
- Upload: `POST /api/v1/admin/uploads`

The API is not yet connected end-to-end to the public website. Keep the current static content until API hosting, login, CRUD and upload tests pass. Never commit secrets, database files or confidential employer/customer information.
