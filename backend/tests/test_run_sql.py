from fastapi.testclient import TestClient


def test_run_sql(client: TestClient):
    payload = {"sql": "SELECT NAME, CLASS, SECTION, MARKS FROM STUDENT;"}
    resp = client.post("/api/v1/sql", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "rows" in body
    assert isinstance(body["rows"], list)
