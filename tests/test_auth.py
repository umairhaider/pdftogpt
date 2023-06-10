import pytest
from fastapi.testclient import TestClient
import os

from main import app

client = TestClient(app)

username = os.environ.get("USERNAME_SECRET")
password = os.environ.get("PASSWORD_SECRET")

@pytest.fixture(scope="module")
def access_token():
    response = client.post("/signin/", data={"username": username, "password": password})
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    yield access_token

def test_sign_in_success():
    response = client.post("/signin/", data={"username": username, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

def test_sign_in_invalid_credentials():
    response = client.post("/signin/", data={"username": "unclebob", "password": "cleancode"})
    assert response.status_code == 401
    assert "detail" in response.json()

def test_jwt_token_validation(access_token):
    response = client.post("/protected_endpoint/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Authorized"

def test_jwt_token_invalid():
    response = client.post("/protected_endpoint/", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
    assert "detail" in response.json()
