from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_ask_question_valid():
    # Upload a PDF file first (ensure this test runs after the upload test)
    with open("test.pdf", "rb") as f:
        client.post("/upload_pdf/", files={"file": f})

    response = client.post("/ask_question/", json={"question": "What is the main idea of the document?"})

    assert response.status_code == 200
    assert "question" in response.json()
    assert "answer" in response.json()

def test_ask_question_invalid():
    # Test without uploading a PDF file first
    response = client.post("/ask_question/", json={"question": "What is the main idea of the document?"})

    assert response.status_code == 400
    assert "detail" in response.json()