from app.utils.sql_cleaner import clean_sql_query


def test_clean_sql_query_removes_markdown_and_adds_semicolon():
    raw = """
```sql
SELECT * FROM STUDENT
```
"""
    cleaned = clean_sql_query(raw)
    assert cleaned == "SELECT * FROM STUDENT;"


def test_clean_sql_query_preserves_semicolon():
    raw = "SELECT COUNT(*) FROM STUDENT;"
    assert clean_sql_query(raw) == raw
