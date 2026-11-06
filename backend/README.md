# Nityanand Portfolio API

FastAPI service for portfolio content, admin authentication, project management and media uploads.

## Production architecture
- Public website: GitHub Pages — https://circuittocode.github.io/
- API: Render Web Service (Singapore)
- Database: managed Render PostgreSQL
- Uploads: persistent Render disk mounted at `/var/data`
- Authentication: short-lived JWT bearer tokens and Argon2 password hashes
- The Render Blueprint is at the repository root: `render.yaml`

## Deploy on Render
1. Push this repository to GitHub (the Blueprint is already in the repository).
2. In Render, choose **New → Blueprint** and connect `CircuitToCode/CircuitToCode.github.io`.
3. Review the resources in `render.yaml`: one API service and one PostgreSQL database. The API uses a paid Starter instance and the database uses the Basic 256 MB plan; Render pricing can change, so review the current cost before applying.
4. When prompted for `ADMIN_PASSWORD_HASH`, provide an Argon2 hash, not a plaintext password. Generate it locally:
   ```bash
   python -c "from pwdlib import PasswordHash; print(PasswordHash.recommended().hash('YOUR-STRONG-PASSWORD'))"
   ```
5. Apply the Blueprint. Render generates `JWT_SECRET` and injects the private database connection string.
6. After deployment, open `https://YOUR-RENDER-SERVICE.onrender.com/health`. It should return JSON with `"status": "ok"`.
7. Open `/docs` to inspect the API. Do not connect the public site to the API until the health check, login, CRUD and upload tests pass.

## Local setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell: .venv\\Scripts\\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   ```
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`; set unique `JWT_SECRET` and `ADMIN_PASSWORD_HASH` values.
4. Start from this `backend` directory: `uvicorn app.main:app --reload`.
5. API docs: `http://127.0.0.1:8000/docs`.

## API
- `GET /health`
- Public: `GET /api/v1/projects`, `GET /api/v1/projects/{slug}`, `GET /api/v1/skills`, `GET /api/v1/experience`, `GET /api/v1/achievements`, `GET /api/v1/profile/{key}`
- Auth: `POST /api/v1/auth/login`
- Admin CRUD: `/api/v1/admin/projects`, `skills`, `experience`, `achievements`, `profile/{key}`
- Upload: `POST /api/v1/admin/uploads`

## Important deployment notes
- GitHub Pages cannot host FastAPI or PostgreSQL; keep it as the static frontend.
- The Render Blueprint creates paid resources. Review Render's current prices before applying.
- Uploads are stored on the persistent disk; database backups and access controls should be configured in Render.
- The API is not yet wired into the public portfolio UI. Keep the existing site and existing admin workflow active until API integration and end-to-end tests are completed.
- Never commit `.env`, passwords, database URLs, JWT secrets or private documents.
