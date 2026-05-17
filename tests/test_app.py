import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

def test_home_endpoint():
    try:
        from main import app
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")
    
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_health_endpoint():
    try:
        from main import app
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")
    
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"