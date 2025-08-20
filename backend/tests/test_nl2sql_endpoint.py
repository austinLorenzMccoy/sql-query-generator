from fastapi.testclient import TestClient
import app.services.nl2sql as nl2sql


def test_nl2sql_endpoint_with_monkeypatch(client: TestClient, monkeypatch):
    def fake_generate_sql(question: str) -> str:
        assert question == "How many entries?"
        return "SELECT COUNT(*) FROM STUDENT;"

    monkeypatch.setattr(nl2sql, "generate_sql", fake_generate_sql)

    resp = client.post("/api/v1/nl2sql", json={"question": "How many entries?"})
    assert resp.status_code == 200
    assert resp.json() == {"sql": "SELECT COUNT(*) FROM STUDENT;"}
