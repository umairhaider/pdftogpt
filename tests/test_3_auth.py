import pytest
from fastapi.testclient import TestClient
import os

from main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def access_token():
    username = os.getenv("USERNAME_SECRET")
    password = os.getenv("PASSWORD_SECRET")
    response = client.post("api/v1/signin/", data={"username": username, "password": password})
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    yield access_token

def test_sign_in_success():
    username = os.getenv("USERNAME_SECRET")
    password = os.getenv("PASSWORD_SECRET")
    response = client.post("api/v1/signin/", data={"username": username, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

def test_sign_in_invalid_credentials():
    response = client.post("api/v1/signin/", data={"username": "unclebob", "password": "cleancode"})
    assert response.status_code == 401
    assert "detail" in response.json()

def test_jwt_token_validation(access_token):
    # Upload a PDF file first (ensure this test runs after the upload test)
    with open("tests/test.pdf", "rb") as f:
        response = client.post("api/v1/upload_pdf/", files={"file": f},
                               headers={"Authorization": f"Bearer {access_token}"})
      
    assert response.status_code == 200
    assert "text" in response.json()

def test_jwt_token_invalid():
    response = client.post("api/v1/ask_question/?question=What is the main idea of the document?",
                           headers={"Authorization": f"Bearer invalidToken"})
        
    assert response.status_code == 401
    assert "detail" in response.json()
