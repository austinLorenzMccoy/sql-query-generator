# Text-to-SQL Platform (FastAPI + Groq) 🚀

This repository provides a modular backend that converts natural language into SQL and executes it on an SQLite database (`school.db`).

The backend is built with FastAPI and uses Groq’s OpenAI-compatible API to generate SQL from English questions. A separate modern UI will be added by the frontend team.

![build](https://img.shields.io/badge/build-passing-brightgreen)
![tests](https://img.shields.io/badge/tests-100%20pass-green)
![coverage](https://img.shields.io/badge/coverage-79%25-yellow)
![fastapi](https://img.shields.io/badge/FastAPI-0.116-009688?logo=fastapi)
![python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![license](https://img.shields.io/badge/license-MIT-blue)

## Table of Contents

- [Features](#features-)
- [Technologies Used](#technologies-used-)
- [Getting Started](#getting-started-)
- [Example Queries](#example-queries)
- [Database Schema](#database-schema-)
- [Architecture](#architecture-)
- [Demo](#demo-)
- [API Endpoints (v1)](#api-endpoints-v1-)
- [Testing & Coverage](#testing--coverage-)
- [Roadmap](#roadmap-)
- [Contributing](#contributing-)

## Features ✨

- Convert natural language questions into SQL queries (Groq).
- Execute generated SQL queries against the SQLite database.
- Clean SQL responses (strip markdown, enforce semicolon).
- Modern FastAPI backend with auto docs at `/docs`.
- Full test suite with coverage and temporary DB isolation.

## Technologies Used 🧰

- [FastAPI](https://fastapi.tiangolo.com/) for the backend API
- [Groq](https://groq.com/) for NL→SQL (OpenAI-compatible API)
- [SQLite](https://www.sqlite.org/) for the demo database
- [Pydantic](https://docs.pydantic.dev/) for validation
- [Pytest](https://docs.pytest.org/) for testing and coverage

## Getting Started 🛠️

Backend is located in `backend/`. You can use Conda for a reproducible setup.

1) Create environment (Option A: from file)
```bash
conda env create -f backend/environment.yml
conda activate text2sql-backend
```

Or Option B (manual):
```bash
conda create -n text2sql-backend python=3.11 -y
conda activate text2sql-backend
pip install -e backend[dev]
```

2) Configure environment variables
```bash
cp backend/.env.example backend/.env
# edit backend/.env and set GROQ_API_KEY and (optionally) GROQ_MODEL
```

2.5) Seed the database (creates/refreshes `school.db`)
```bash
python backend/scripts/seed_db.py
```

3) Run the API (from repo root)
```bash
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

Open API docs at: http://127.0.0.1:8000/docs

## Example Queries

Here are some example questions you can ask:

- "How many entries of records are present?"
- "Tell me all the students studying in Data Science class?"
- "What is the average marks of students?"

## Database Schema

The database **school.db** has the following schema:

| Column  | Type    | Description                          |
|---------|---------|--------------------------------------|
| NAME    | VARCHAR(25) | Name of the student                  |
| CLASS   | VARCHAR(25) | Class of the student                 |
| SECTION | VARCHAR(25) | Section of the student               |
| MARKS   | INT     | Marks obtained by the student        |

## Architecture 🧩

```
┌──────────────────────────────────────────────────────────────┐
│                      Client (future SPA)                      │
└──────────────▲───────────────────────────────────────▲───────┘
               │                                       │
               │ HTTP (JSON)                           │
               │                                       │
        ┌──────┴───────────────────────────────────────┴──────┐
        │                     FastAPI Backend                   │
        │                 `backend/app/main.py`                 │
        ├───────────────┬───────────────────────────┬──────────┤
        │ API (v1)      │ Services                  │ Utils     │
        │ routes.py     │ - nl2sql.py (Groq)        │ - sql_cleaner.py
        │               │ - db.py (SQLite ops)      │          │
        └───────────────┴───────────────┬───────────┴──────────┘
                                        │
                                        │ SQL
                                        ▼
                                 SQLite: school.db
```

## Demo ▶️

- Start server from repo root:
  ```bash
  uvicorn app.main:app --reload --port 8000 --app-dir backend
  ```
- Run the demo script:
  ```bash
  python backend/api_demo.py
  ```

## API Endpoints (v1) 📡

- GET `/api/v1/health` → health check
- GET `/api/v1/students` → list all students
- POST `/api/v1/sql` → execute provided SQL
- POST `/api/v1/nl2sql` → convert NL to SQL using Groq

Example curl (after starting the server):
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

## Testing & Coverage 🧪

```bash
cd backend
pytest -q --cov=app --cov-report=term-missing
```

Tests use a temporary SQLite DB and do not touch your real `school.db`.

## Roadmap 🗺️

- Frontend UI integration (modern SPA)
- AuthN/Z and rate limiting
- Schema introspection and multi-table support
- Safer SQL generation and validation guardrails

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you'd like to contribute.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License.
