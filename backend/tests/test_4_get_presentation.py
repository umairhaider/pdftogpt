from fastapi.testclient import TestClient
import pytest
import os
from main import app
import time
from app.service.knowledgebase_handler import set_knowledge_base

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_context():
    set_knowledge_base(None)  # Reset the context to an empty string
    yield  # Yield to allow the test to run
    set_knowledge_base(None)  # Reset the context again after the test completes

@pytest.fixture(scope="module")
def access_token():
    username = os.getenv("USERNAME_SECRET")
    password = os.getenv("PASSWORD_SECRET")
    response = client.post("api/v1/signin/", data={"username": username, "password": password})
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    yield access_token

def test_get_presentation_valid(access_token):
    # Upload a PDF file first (ensure this test runs after the upload test)
    with open("tests/test.pdf", "rb") as f:
        client.post("api/v1/upload_pdf/", files={"file": f},
                           headers={"Authorization": f"Bearer {access_token}"})
    
    print("Waiting for PDF to be processed...")
    # Wait for a brief moment to allow for processing
    time.sleep(5)

    # Assuming the user is authenticated
    response = client.post("api/v1/get_presentation/",
                               headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    assert "presentation.pptx" in response.headers["Content-Disposition"]

def test_get_presentation_no_pdf_invalid(access_token):
    # Test PPTX without uploading a PDF file first
    response = client.post("api/v1/get_presentation/",
                           headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 400
    assert "detail" in response.json()

def test_get_presentation_endpoint_unauthenticated():
    # Assuming the user is not authenticated
    response = client.post("api/v1/get_presentation/")

    #Forbidden 403 Response
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"
