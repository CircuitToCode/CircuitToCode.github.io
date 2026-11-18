# Nityanand Portfolio — Architecture & Delivery Plan

## Product goal
A cinematic, recruiter-first engineering portfolio with an editable content system. The visual identity uses midnight navy/black, controlled neon red and violet light, glass panels, oversized typography and motion that respects reduced-motion settings.

## Free/open-source architecture
1. Public frontend: GitHub Pages, using the existing static HTML/CSS/JavaScript codebase.
2. API: FastAPI, self-hosted in Docker.
3. Database: SQLite in a persistent Docker volume for the zero-cost starter deployment. PostgreSQL remains an optional open-source migration on a self-hosted server.
4. Authentication: short-lived JWT bearer tokens and Argon2 password hashes; secrets only in environment variables.
5. Uploads: validated JPG/PNG/WebP/PDF files stored in a persistent local Docker volume.
6. Admin: retain the existing dashboard; connect it to FastAPI only after a reachable HTTPS API endpoint is configured and tested.

No paid hosting, paid managed database, paid API, or mandatory subscription is part of the plan. GitHub Pages hosts static frontend files only; it cannot run FastAPI or a persistent database. Public remote access therefore requires an always-on self-hosted computer/server with HTTPS.

## Database schema
- projects: slug, title, description, category, technologies JSON, status, image URL, gallery JSON, GitHub/demo URLs, featured, sort order, published.
- skills: name, category, proficiency, sort order.
- experience: role, company, period, location, responsibilities JSON, contributions JSON, sort order.
- achievements: label, detail, optional metric, sort order.
- site_profile: unique key and JSON value for editable about, education, career goals and social links.

## API contract
- GET /health
- POST /api/v1/auth/login
- GET /api/v1/projects?category=&search=
- GET /api/v1/projects/{slug}
- GET /api/v1/skills
- GET /api/v1/experience
- GET /api/v1/achievements
- GET /api/v1/profile/{key}
- POST/PUT/DELETE /api/v1/admin/projects
- POST/PUT/DELETE /api/v1/admin/skills
- POST/PUT/DELETE /api/v1/admin/experience
- POST/PUT/DELETE /api/v1/admin/achievements
- PUT /api/v1/admin/profile/{key}
- POST /api/v1/admin/uploads

All /admin routes require a valid bearer token. Public routes expose only published projects.

## Content integrity
Do not invent completed projects or quantified manufacturing results. Label concepts, prototypes and work-in-progress accurately. Do not publish confidential employer/customer drawings, process recipes, proprietary production data or private reports.

## Release gates
1. Local backend boot, health check, login, CRUD and upload tests.
2. Frontend visual and responsive QA at desktop/tablet/mobile widths.
3. Self-hosted API configured with HTTPS and CORS restricted to the portfolio origin.
4. Admin login, image upload, project edit and public-site refresh verified end-to-end.
5. GitHub Pages build and deployment confirmed successful.
