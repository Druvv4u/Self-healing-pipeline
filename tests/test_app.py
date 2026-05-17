import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

def test_imports():
    """This will fail if any import in main.py is broken"""
    import importlib
    import main
    importlib.reload(main)

def test_home_endpoint():
    from main import app
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_health_endpoint():
    from main import app
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"