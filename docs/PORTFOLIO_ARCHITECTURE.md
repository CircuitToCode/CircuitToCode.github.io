# Nityanand Portfolio — Architecture & Delivery Plan

## Product goal
A cinematic, recruiter-first engineering portfolio with an editable content system. The public site is a digital experience, not a static CV. The visual identity uses midnight navy/black, controlled neon red and violet light, glass panels, oversized typography and motion that respects reduced-motion settings.

## Current repository baseline
- GitHub Pages frontend at https://circuittocode.github.io/
- Existing cinematic homepage, project archive and five case-study pages.
- Existing PNG portrait at assets/nityanand-portrait.png.
- Existing live public GitHub activity feed.
- Existing Cloudflare Worker admin API is a separate deployed service.
- New FastAPI backend scaffold lives in /backend.

## Target architecture
1. Public frontend: static deployable web client. Keep GitHub Pages as the public host for the first release; use semantic HTML/CSS/JavaScript modules for the current codebase. A React/Vite migration can be introduced as a separate build step after parity is verified, rather than breaking the live Pages site.
2. API: FastAPI under /backend. It exposes public read endpoints and protected admin write endpoints.
3. Database: SQLAlchemy models support SQLite for local development and PostgreSQL through DATABASE_URL in production.
4. Authentication: short-lived JWT bearer tokens, Argon2 password hashes, secrets supplied only through environment variables.
5. Uploads: validated JPG/PNG/WebP/PDF uploads stored outside source control on a persistent-volume host.
6. Admin: keep the existing Cloudflare Worker admin entrypoint until the new API is deployed and its login, CRUD and upload flows are tested. Never expose service secrets in browser JavaScript.

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

## Website sections
- Cinematic intro and ENTER PORTFOLIO action
- Visitor pathways: recruiter, engineering professional, collaborator, developer
- Split hero with portrait, resume, LinkedIn and GitHub
- Engineering journey and education timeline
- Achievement highlights (only verified metrics; no invented counts)
- Filterable skills universe
- About and career direction
- Searchable, category-filtered project universe with individual case studies
- Experience and achievements
- Cinematic “To be continued” ending and contact CTA

## Content integrity
The portfolio owner has approximately one year of professional experience. Do not invent 50+ completed projects or quantified manufacturing results. The “50+ projects” figure is a user-supplied target claim and must be confirmed before it is published as a factual statistic. Use clearly labelled concepts, prototypes and work-in-progress status where appropriate. Do not publish confidential employer/customer drawings, process recipes, proprietary production data or private reports.

## Deployment boundaries
GitHub Pages serves static files only; it does not execute FastAPI or host a persistent SQLite database. The API must be deployed separately with HTTPS, environment secrets and persistent storage. Use PostgreSQL for production. Set the frontend API base URL only after the API host is selected and health-checked.

## Release gates
1. Local backend boot, health check, login, CRUD and upload tests.
2. Frontend visual and responsive QA at desktop/tablet/mobile widths.
3. API host provisioned; CORS restricted to the portfolio origin.
4. Admin login, image upload, project edit and public-site refresh verified end-to-end.
5. GitHub Pages build and deployment confirmed successful.
