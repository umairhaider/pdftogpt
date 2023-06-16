from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app
import pytest
from unittest.mock import patch
from app.service.pptx_hander import process_presentation, generate_presentation, validate_json_data_structure


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
    with pytest.raises(HTTPException) as e:
        process_presentation(json_data)
    assert str(e.value.detail) == "Invalid JSON data format"

    json_data = 123
    with pytest.raises(HTTPException) as e:
        process_presentation(json_data)
    assert str(e.value.detail) == "Invalid JSON data format"

    json_data = {"slides": "invalid"}
    with pytest.raises(HTTPException) as e:
        process_presentation(json_data)
    assert str(e.value.detail) == "Invalid JSON data format"

    json_data = {"slides": [{"title": "Slide 1", "content": "Content of Slide 1"}, "invalid"]}
    with pytest.raises(HTTPException) as e:
        process_presentation(json_data)
    assert str(e.value.detail) == "Invalid JSON data format"

@pytest.mark.asyncio
@patch("app.service.pptx_hander.process_user_question")
@patch("app.service.pptx_hander.get_knowledge_base")
async def test_generate_presentation_exception(mock_get_knowledge_base, mock_process_user_question):
    """
    Test that generate_presentation function does not raise an exception when a valid context is available.
    """
    mock_get_knowledge_base.return_value = "Mock knowledge base"
    mock_process_user_question.side_effect = Exception("Unexpected error")

    with pytest.raises(HTTPException) as e_info:
        await generate_presentation()

    assert e_info.value.status_code == 500
    assert e_info.value.detail == "Unexpected error"


def test_validate_json_data_structure():
    # Case 1: Invalid JSON data format (not dict or list)
    with pytest.raises(ValueError) as e_info:
        validate_json_data_structure("invalid_data")
    assert str(e_info.value) == "Invalid JSON data format"

    # Case 2: Valid JSON data format (dict) but missing 'slides' field
    json_data = {"key": "value"}
    with pytest.raises(ValueError) as e_info:
        validate_json_data_structure(json_data)
    assert str(e_info.value) == "Missing 'slides' field in slide data"

    # Case 3: Valid JSON data format (dict) with 'slides' field but invalid slide data
    json_data = {"slides": "invalid_slide_data"}
    with pytest.raises(ValueError) as e_info:
        validate_json_data_structure(json_data)
    assert str(e_info.value) == "Invalid JSON data format"

    # Case 4: Valid slide data with missing 'title' field
    json_data = [{"content": "Slide content"}]
    with pytest.raises(ValueError) as e_info:
        validate_json_data_structure(json_data)
    assert str(e_info.value) == "Missing 'title' field in slide data"

    # Case 5: Valid slide data with 'title' field but not a string
    json_data = [{"title": 123, "content": "Slide content"}]
    with pytest.raises(ValueError) as e_info:
        validate_json_data_structure(json_data)
    assert str(e_info.value) == "'title' field must be a string"

    # Case 6: Valid slide data with missing 'content' field
    json_data = [{"title": "Slide title"}]
    with pytest.raises(ValueError) as e_info:
        validate_json_data_structure(json_data)
    assert str(e_info.value) == "Missing 'content' field in slide data"

    # Case 7: Valid slide data with 'content' field but not a string
    json_data = [{"title": "Slide title", "content": 123}]
    with pytest.raises(ValueError) as e_info:
        validate_json_data_structure(json_data)
    assert str(e_info.value) == "'content' field must be a string"

    # Case 8: Valid JSON data format (list) with multiple valid slide data
    json_data = [
        {"title": "Slide 1", "content": "Slide 1 content"},
        {"title": "Slide 2", "content": "Slide 2 content"},
    ]
    validate_json_data_structure(json_data)  # No exception should be raised
