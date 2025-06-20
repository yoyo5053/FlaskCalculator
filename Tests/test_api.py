import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_api_addition_success(client):
    payload = {"num1": "10", "num2": "5", "operation": "add"}
    rv = client.post("/api/calculate/", json=payload)
    assert rv.status_code == 200
    data = rv.get_json()
    assert "result" in data
    assert data["result"] == "15"

def test_api_division_par_zero(client):
    payload = {"num1": "5", "num2": "0", "operation": "divide"}
    rv = client.post("/api/calculate/", json=payload)
    assert rv.status_code == 200
    data = rv.get_json()
    assert "result" in data
    assert data["result"] == "0"

def test_api_invalid_input(client):
    payload = {"num1": "foo", "num2": "2", "operation": "add"}
    rv = client.post("/api/calculate/", json=payload)
    assert rv.status_code == 400
    data = rv.get_json()
    assert "Invalid input" in data["message"]

def test_api_invalid_operation(client):
    payload = {"num1": "1", "num2": "2", "operation": "mod"}
    rv = client.post("/api/calculate/", json=payload)
    assert rv.status_code == 400
    data = rv.get_json()
    assert "Invalid operation" in data["message"]
