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

@pytest.mark.order(3)
def test_03_upload_pdf_valid(access_token):
    # Create a sample PDF file object for testing
    with open("test.pdf", "rb") as f:
        response = client.post("api/v1/upload_pdf/", files={"file": f},
                               headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert "text" in response.json()
    assert "generated_text" in response.json()
@pytest.mark.order(4)
def test_04_upload_pdf_invalid(access_token):
    # Create a sample non-PDF file object for testing
    with open("test.txt", "rb") as f:
        response = client.post("api/v1/upload_pdf/", files={"file": f},
                               headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 400
    assert "detail" in response.json()