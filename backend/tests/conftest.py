import os
import sqlite3
import tempfile
import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(scope="session")
def temp_db_path():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    # initialize schema and seed data
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS STUDENT (
            NAME TEXT,
            CLASS TEXT,
            SECTION TEXT,
            MARKS INTEGER
        );
        """
    )
    cur.executemany(
        "INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?,?,?,?)",
        [
            ("Krish", "Data Science", "A", 90),
            ("Sudhanshu", "Data Science", "B", 100),
            ("Darius", "Data Science", "A", 86),
            ("Vikash", "DEVOPS", "A", 50),
            ("Dipesh", "DEVOPS", "A", 35),
        ],
    )
    conn.commit()
    conn.close()
    yield path
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


@pytest.fixture(autouse=True)
def _env_sqlite(temp_db_path, monkeypatch):
    monkeypatch.setenv("SQLITE_PATH", temp_db_path)


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    return TestClient(app)
