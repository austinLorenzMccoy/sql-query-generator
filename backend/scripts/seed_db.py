#!/usr/bin/env python3
"""
Seed the demo SQLite database with the STUDENT table and sample rows.

- Resolves DB path via app settings (SQLITE_PATH or default 'school.db').
- Safe to run multiple times; it truncates STUDENT before inserting.

Usage:
  python backend/scripts/seed_db.py
Optionally set SQLITE_PATH in environment or backend/.env.
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

# Ensure app can be imported when executed from repo root
# (uvicorn uses --app-dir backend, but scripts may run from root)
import sys
REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import get_settings  # type: ignore  # noqa: E402


def main() -> None:
    settings = get_settings()
    db_path = os.environ.get("SQLITE_PATH", settings.sqlite_path)
    db_path = str(Path(db_path))

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS STUDENT (
              NAME    VARCHAR(25),
              CLASS   VARCHAR(25),
              SECTION VARCHAR(25),
              MARKS   INT
            );
            """
        )
        # Clear existing rows to keep the seed idempotent
        cur.execute("DELETE FROM STUDENT;")
        cur.executemany(
            "INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?);",
            [
                ("Alice", "Data Science", "A", 85),
                ("Bob", "Data Science", "B", 78),
                ("Charlie", "AI", "A", 92),
                ("Diana", "AI", "B", 88),
            ],
        )
        conn.commit()
        print(f"Seeded STUDENT table in {db_path} with 4 rows.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
