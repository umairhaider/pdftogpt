from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import app.service.pdf_handler as pdf_handler
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

@pytest.mark.asyncio
@patch("pdfplumber.open")
async def test_generate_presentation_exception(mock_open):
    """
    Test that generate_presentation function does not raise an exception when a valid context is available.
    """
    file = MagicMock()
    file.content_type = "application/pdf"
    mock_open.side_effect = Exception("Unexpected error")

    with pytest.raises(HTTPException) as e_info:
        await pdf_handler.upload_pdf(file)

    assert e_info.value.status_code == 500
    assert e_info.value.detail == "Unexpected error"