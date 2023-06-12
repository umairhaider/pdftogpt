from fastapi.testclient import TestClient
from main import app
import pytest
from app.service.pptx_hander import process_presentation


client = TestClient(app)

def test_process_presentation_with_dict_data():
    json_data = {
        "slides": [
            {
                "title": "Slide 1",
                "content": "Content of Slide 1"
            },
            {
                "title": "Slide 2",
                "content": "Content of Slide 2"
            }
        ]
    }
    output_file = process_presentation(json_data)
    assert output_file == "presentation.pptx"

def test_process_presentation_with_list_data():
    json_data = [
        {
            "title": "Slide 1",
            "content": "Content of Slide 1"
        },
        {
            "title": "Slide 2",
            "content": "Content of Slide 2"
        }
    ]
    output_file = process_presentation(json_data)
    assert output_file == "presentation.pptx"

def test_process_presentation_with_invalid_data():
    json_data = "invalid"
    with pytest.raises(ValueError) as e:
        process_presentation(json_data)
    assert str(e.value) == "Invalid JSON data format"

    json_data = 123
    with pytest.raises(ValueError) as e:
        process_presentation(json_data)
    assert str(e.value) == "Invalid JSON data format"

    json_data = {"slides": "invalid"}
    with pytest.raises(ValueError) as e:
        process_presentation(json_data)
    assert str(e.value) == "Invalid JSON data format"

    json_data = {"slides": [{"title": "Slide 1", "content": "Content of Slide 1"}, "invalid"]}
    with pytest.raises(ValueError) as e:
        process_presentation(json_data)
    assert str(e.value) == "Invalid JSON data format"

