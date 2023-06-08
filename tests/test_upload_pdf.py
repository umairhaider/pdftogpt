from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)


@pytest.mark.order(3)
def test_03_upload_pdf_valid():
    # Create a sample PDF file object for testing
    with open("test.pdf", "rb") as f:
        response = client.post("/upload_pdf/", files={"file": f})
    
    assert response.status_code == 200
    assert "text" in response.json()
    assert "generated_text" in response.json()
@pytest.mark.order(4)
def test_04_upload_pdf_invalid():
    # Create a sample non-PDF file object for testing
    with open("test.txt", "rb") as f:
        response = client.post("/upload_pdf/", files={"file": f})
    
    assert response.status_code == 400
    assert "detail" in response.json()