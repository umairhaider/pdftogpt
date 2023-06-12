from fastapi.testclient import TestClient
import pytest
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

def test_upload_pdf_valid(access_token):
    # Create a sample PDF file object for testing
    with open("tests/test.pdf", "rb") as f:
        response = client.post("api/v1/upload_pdf/", files={"file": f},
                               headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert "text" in response.json()
    assert "generated_text" in response.json()

def test_upload_pdf_invalid(access_token):
    # Create a sample non-PDF file object for testing
    with open("tests/test.txt", "rb") as f:
        response = client.post("api/v1/upload_pdf/", files={"file": f},
                               headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 400
    assert "detail" in response.json()


def test_upload_pdf_with_pages_valid(access_token):
    # Create a sample PDF file object for testing
    with open("tests/test_multiple_valid.pdf", "rb") as f:
        response = client.post("api/v1/upload_pdf/", files={"file": f},
                               headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert "text" in response.json()
    assert "generated_text" in response.json()