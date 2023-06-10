from fastapi.testclient import TestClient
import time
import pytest
import os

from main import app

client = TestClient(app)

username = os.environ.get("USERNAME_SECRET")
password = os.environ.get("PASSWORD_SECRET")

@pytest.fixture(scope="module")
def access_token():
    response = client.post("api/v1/signin/", data={"username": username, "password": password})
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    yield access_token

@pytest.mark.order(1)
def test_01_ask_question_invalid(access_token):
    # Test without uploading a PDF file first
    response = client.post("api/v1/ask_question/?question=What is the main idea of the document?",
                           headers={"Authorization": f"Bearer {access_token}"})
    

    assert response.status_code == 400
    assert "detail" in response.json()
    
@pytest.mark.order(2)
def test_02_ask_question_valid(access_token):
    # Upload a PDF file first (ensure this test runs after the upload test)
    with open("test.pdf", "rb") as f:
        client.post("api/v1/upload_pdf/", files={"file": f},
                           headers={"Authorization": f"Bearer {access_token}"})
    
    print("Waiting for PDF to be processed...")
    # Wait for a brief moment to allow for processing
    time.sleep(5)

    response = client.post("api/v1/ask_question/?question=What is the main idea of the document?",
                           headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert "question" in response.json()
    assert "answer" in response.json()