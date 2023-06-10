from fastapi.testclient import TestClient
import time
import pytest
import os

from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def access_token():
    username = os.environ.get("USERNAME_SECRET")
    password = os.environ.get("PASSWORD_SECRET")
    response = client.post("/signin/", data={"username": username, "password": password})
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    yield access_token

@pytest.mark.order(1)
def test_01_ask_question_invalid():
    # Test without uploading a PDF file first
    response = client.post("/ask_question/?question=What is the main idea of the document?",
                           headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 400
    assert "detail" in response.json()
    
@pytest.mark.order(2)
def test_02_ask_question_valid():
    # Upload a PDF file first (ensure this test runs after the upload test)
    with open("test.pdf", "rb") as f:
        client.post("/upload_pdf/", files={"file": f})
    
    print("Waiting for PDF to be processed...")
    # Wait for a brief moment to allow for processing
    time.sleep(5)

    response = client.post("/ask_question/?question=What is the main idea of the document?",
                           headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert "question" in response.json()
    assert "answer" in response.json()