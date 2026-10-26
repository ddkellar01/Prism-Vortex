from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Validates cluster readiness health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "PrismVortex"


def test_scout_endpoint_payload_validation():
    """Validates that malformed payloads return appropriate HTTP validation errors."""
    response = client.post("/v1/scout", json={"invalid_field": "test"})
    assert response.status_code == 422