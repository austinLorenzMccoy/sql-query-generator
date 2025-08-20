# Product Requirements Document (PRD)

Project: Text-to-SQL Platform (FastAPI + Groq)
Codebase root: `/Users/a/Documents/DataScience_World/LLM_project/TextToSQLapp`

## 1) Overview
The Text-to-SQL platform converts natural language questions into SQL, executes the SQL against an SQLite database (`school.db`), and exposes results via a REST API.

- Backend: FastAPI
- NL→SQL: Groq (OpenAI-compatible API)
- DB: SQLite (demo), path configurable via `.env` or env var `SQLITE_PATH`

## 2) Goals
- Reliable API endpoints for health, data access, direct SQL execution, and NL→SQL.
- Reproducible local environment via Conda.
- Clear docs and demo script.
- Maintainable code with tests and useful coverage (≥75%).

## 3) Non-Goals
- Full production-grade UI (future).
- RBAC/SSO and multi-tenant auth (future).
- Non-SQLite backends (future).

## 4) Users
- Data analysts, educators, and developers needing quick NL→SQL.

## 5) Success Metrics
- P0: Endpoints return correct shapes and sensible error messages.
- P0: Local tests pass with coverage ≥ 75%.
- P1: NL2SQL produces valid SQL for common demo questions.
- P1: p95 NL2SQL latency < 3s (network and LLM dependent).

## 6) Architecture
- App entry: `backend/app/main.py`
- Routes: `backend/app/api/v1/routes.py`
- Config: `backend/app/core/config.py` (Pydantic Settings)
- Services: `backend/app/services/`
  - `db.py` (SQLite operations)
  - `nl2sql.py` (Groq calls)
- Utils: `backend/app/utils/sql_cleaner.py`
- Models/schemas: `backend/app/models/schemas.py`
- Tests: `backend/tests/`
- Demo: `backend/api_demo.py`

## 7) Functional Requirements
- GET `/api/v1/health` → `{ "status": "ok" }`
- GET `/api/v1/students` → returns rows from `STUDENT` table
- POST `/api/v1/sql` with `{ "sql": "..." }` → returns `rows` or `rowcount`
- POST `/api/v1/nl2sql` with `{ "question": "..." }` → returns `{ "sql": "..." }`

## 8) Non-Functional Requirements
- Reliability: robust error handling for DB and LLM failures.
- Security: `.env` ignored; no secrets in logs; basic SQL cleaning.
- Observability: structured logs.
- Performance: appropriate for SQLite; minimal overhead.
- Maintainability: typed Python, tests, organized modules.

## 9) API Spec (v1)
Base: `/api/v1`

- `GET /health` → 200 `{ "status": "ok" }`
- `GET /students` → 200 `{ "rows": [[...], ...] }` | 200 `{ "rows": [] }`
- `POST /sql` → 200 `{ "rows": [[...]] }` or `{ "rowcount": N }`, 400 on invalid SQL
- `POST /nl2sql` → 200 `{ "sql": "SELECT ...;" }`, 502 on LLM error

## 10) Data Model
SQLite file: `school.db`
- Table: `STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)`

## 11) Configuration
- `backend/.env.example` → copy to `backend/.env`
- Vars:
  - `GROQ_API_KEY` (required for NL2SQL)
  - `GROQ_MODEL` (default `llama-3.1-70b-versatile`)
  - `SQLITE_PATH` (default `school.db`)

## 12) Dependencies
- Declared in `backend/environment.yml` and `backend/pyproject.toml`.
- Key: fastapi, uvicorn, groq, pydantic, pydantic-settings, python-dotenv, pytest, pytest-cov, httpx, ruff.

## 13) Security & Privacy
- No secret commits.
- Clean LLM outputs to SQL (strip markdown, ensure semicolon).
- Future: schema allow-listing and stricter SQL validation.

## 14) Testing
- Unit/integration tests in `backend/tests/`.
- Temporary DB per test where needed; avoid mutating real `student.db`.
- Goal: keep coverage ≥ 75% (current ~79%).

## 15) Observability
- Logging set in `backend/app/core/logging.py`.
- Future: request IDs and tracing hooks.

## 16) Deployment
- Local: `uvicorn app.main:app --reload --port 8000 --app-dir backend`
- Future: containerization and CI deploys.

## 17) Risks & Mitigations
- LLM hallucination → cleaning and guardrails; schema awareness later.
- Missing DB → seed script and clear errors.
- API key missing → error with actionable message.
- README divergence → maintain single source on main and use PRs.

## 18) Rollout Plan
- Phase 1: Backend stable (current)
- Phase 2: Frontend SPA
- Phase 3: Security hardening, schema introspection, Docker/CI

## 19) Timeline (example)
- W1: Stabilize backend, DB seeding, CI
- W2: Frontend prototype
- W3: Improve guardrails and prompts
- W4: Docker & release

## 20) Acceptance Criteria
- Endpoints function as spec’d
- Demo script returns rows and valid NL→SQL
- Tests pass locally/CI; coverage ≥ 75%
- README documents setup and usage

---

# Step-by-Step Implementation Plan

## A) Environment & Setup
1. Create Conda env (first time only):
   ```bash
   conda env create -f backend/environment.yml
   # if env exists:
   conda env update -n text2sql-backend -f backend/environment.yml --prune
   conda activate text2sql-backend
   ```
2. Configure env vars:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env to set GROQ_API_KEY and optionally GROQ_MODEL and SQLITE_PATH
   ```

## B) Database Initialization (demo)
From repo root:
```bash
sqlite3 school.db <<'SQL'
CREATE TABLE IF NOT EXISTS STUDENT (
  NAME    VARCHAR(25),
  CLASS   VARCHAR(25),
  SECTION VARCHAR(25),
  MARKS   INT
);

DELETE FROM STUDENT;

INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES
('Alice','Data Science','A',85),
('Bob','Data Science','B',78),
('Charlie','AI','A',92),
('Diana','AI','B',88);
SQL
```
If you want a different path:
- Set `SQLITE_PATH=/absolute/path/to/school.db` in `backend/.env`

## C) Run the API
```bash
uvicorn app.main:app --reload --port 8000 --app-dir backend
# Docs: http://127.0.0.1:8000/docs
```

## D) Sanity Test (curl)
```bash
curl http://127.0.0.1:8000/api/v1/health
curl http://127.0.0.1:8000/api/v1/students
curl -X POST http://127.0.0.1:8000/api/v1/sql \
  -H 'Content-Type: application/json' \
  -d '{"sql":"SELECT COUNT(*) FROM STUDENT;"}'
```

## E) NL→SQL Demo
```bash
python backend/api_demo.py
```
Requires `GROQ_API_KEY` to be set in `backend/.env`.

## F) Running Tests
```bash
cd backend
pytest -q --cov=app --cov-report=term-missing
```
Expected: All tests pass, coverage ~79%.

## G) Development Workflow
1. Branch from `main`: `git switch -c feature/<name>`
2. Make changes; keep commits focused.
3. Run tests locally.
4. Push branch and open PR.
5. Address review, squash/rebase as appropriate.

## H) Future Enhancements
- Frontend SPA (React/Vue/Svelte) consuming `/api/v1`
- AuthN/Z, rate limiting
- Schema introspection and allow-listed SQL
- Dockerfile + GitHub Actions CI
- Prompt tuning and fallback strategies for NL2SQL

---

# Appendix

## Files & Paths
- App: `backend/app/main.py`
- Routes: `backend/app/api/v1/routes.py`
- Services: `backend/app/services/`
- Config: `backend/app/core/config.py`
- Tests: `backend/tests/`
- Demo: `backend/api_demo.py`
- Environment: `backend/environment.yml`

## Troubleshooting
- "no such table: STUDENT": seed DB (see section B) or set `SQLITE_PATH`.
- 502 from `/nl2sql`: ensure `GROQ_API_KEY` is set and network available.
- Port in use: `lsof -ti:8000 | xargs -r kill -9` then restart.
