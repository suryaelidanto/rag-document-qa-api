from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    if response.status_code == 404:
        response = client.get("/")
    assert response.status_code == 200


def test_rag_query_success():
    payload = {
        "question": "What is AI Engineering?",
        "document_text": "AI Engineering is a professional field focused on building production-grade AI systems.",
    }

    response = client.post("/rag-query", json=payload)
    assert response.status_code == 200
    assert "answer" in response.json()
    assert response.json()["chunks_used"] > 0
