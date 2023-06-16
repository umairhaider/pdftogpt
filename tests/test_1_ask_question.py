from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.service import question_handler
import time
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

def test_ask_question_invalid(access_token):
    # Test without uploading a PDF file first
    response = client.post("api/v1/ask_question/?question=What is the main idea of the document?",
                           headers={"Authorization": f"Bearer {access_token}"})
    

    assert response.status_code == 400
    assert "detail" in response.json()
    
def test_ask_question_valid(access_token):
    # Upload a PDF file first (ensure this test runs after the upload test)
    with open("tests/test.pdf", "rb") as f:
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

@pytest.mark.asyncio
@patch("app.service.question_handler.process_user_question")
@patch("app.service.question_handler.get_knowledge_base")
async def test_ask_question_exception(mock_get_knowledge_base, mock_process_user_question):
    """
    Test that ask_question function raises an exception when an error occurs.
    """
    mock_get_knowledge_base.return_value = MagicMock()
    user_question = "Sample question"
    mock_process_user_question.side_effect = Exception("Unexpected error")

    with pytest.raises(HTTPException) as e_info:
        await question_handler.ask_question(user_question)

    assert e_info.value.status_code == 500
    assert e_info.value.detail == "Unexpected error"