from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
