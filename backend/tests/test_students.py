from fastapi.testclient import TestClient


def test_list_students(client: TestClient):
    resp = client.get("/api/v1/students")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert {"name", "class_name", "section", "marks"}.issubset(data[0].keys())
