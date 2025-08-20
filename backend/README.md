# Text-to-SQL Backend (FastAPI + Groq)

A modular FastAPI backend that converts natural language to SQL for the `STUDENT` table in `school.db` and executes queries safely.

## Project Structure

```
backend/
  app/
    api/v1/
      __init__.py
      routes.py           # /health, /students, /sql, /nl2sql
    core/
      config.py           # Settings via Pydantic + .env
      logging.py          # Basic logging setup
    models/
      schemas.py          # Pydantic models
    services/
      db.py               # SQLite access helpers
      nl2sql.py           # Google Gemini integration
    utils/
      sql_cleaner.py      # Remove markdown, enforce semicolon
    __init__.py
    main.py               # FastAPI factory + include router
  tests/
    conftest.py           # Temp DB per test session
    test_health.py
    test_students.py
    test_sql_cleaner.py
    test_run_sql.py
    test_nl2sql_endpoint.py
  .env.example
  api_demo.py
  pyproject.toml
  setup.py
  README.md
```

## Requirements

- Python 3.9+
- Conda (for environment management)
- SQLite database at `TextToSQLapp/school.db` (can be created/seeded)

## Quickstart (Conda + Uvicorn)

```bash
# from repo root
# Option A: create from environment.yml
conda env create -f backend/environment.yml
conda activate text2sql-backend

# Option B: create manually
# conda create -n text2sql-backend python=3.11 -y
# conda activate text2sql-backend
# pip install -e backend[dev]

# prepare env
cp backend/.env.example backend/.env
# then edit backend/.env and set GROQ_API_KEY

# seed demo database (creates/refreshes `school.db`)
python backend/scripts/seed_db.py

# run API
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

Open: http://127.0.0.1:8000/docs

## Endpoints

- GET `/api/v1/health` → `{ "status": "ok" }`
- GET `/api/v1/students` → list students
- POST `/api/v1/sql` → body `{ "sql": "SELECT ...;" }`
- POST `/api/v1/nl2sql` → body `{ "question": "..." }` returns `{ "sql": "...;" }`

## Curl Demo

```bash
python backend/api_demo.py
```

Or manually:

```bash
curl http://127.0.0.1:8000/api/v1/health
curl http://127.0.0.1:8000/api/v1/students
curl -X POST http://127.0.0.1:8000/api/v1/sql \
  -H 'Content-Type: application/json' \
  -d '{"sql":"SELECT COUNT(*) FROM STUDENT;"}'

curl -X POST http://127.0.0.1:8000/api/v1/nl2sql \
  -H 'Content-Type: application/json' \
  -d '{"question":"How many entries of records are present?"}'
```

## Testing & Coverage

```bash
# from backend/
pytest
# or with full output
pytest -q --cov=app --cov-report=term-missing --cov-report=xml:coverage.xml
```

The test suite uses a temporary SQLite database and does not touch your real `school.db`.

## Configuration

Configuration is handled by `app/core/config.py` using Pydantic BaseSettings:

- `APP_NAME` (default: Text-to-SQL Backend)
- `SQLITE_PATH` (default: school.db)
- `GROQ_API_KEY` (required for /nl2sql)
- `GROQ_MODEL` (default: llama-3.1-70b-versatile)

Env file: `backend/.env` (copy from `.env.example`).

## Notes on NL→SQL

- `app/services/nl2sql.py` integrates Groq via its OpenAI-compatible Chat Completions API.
- `app/utils/sql_cleaner.py` strips markdown and enforces trailing semicolon.
- Tests mock the model so CI can run without an API key.

## Developing

- Linting (optional):
  ```bash
  pip install ruff
  ruff check backend/app
  ```

- Packaging:
  - `pyproject.toml` defines project metadata, test, and coverage settings.
  - `setup.py` provided for compatibility.

