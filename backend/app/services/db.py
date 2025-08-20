import sqlite3
from contextlib import contextmanager
from typing import Any, Iterable, List, Tuple

from ..core.config import get_settings


@contextmanager
def get_connection():
    settings = get_settings()
    conn = sqlite3.connect(settings.sqlite_path)
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(sql: str, params: Iterable[Any] | None = None) -> List[Tuple[Any, ...]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, tuple(params or ()))
        rows = cur.fetchall()
    return rows


def execute(sql: str, params: Iterable[Any] | None = None) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, tuple(params or ()))
        conn.commit()
        return cur.rowcount
