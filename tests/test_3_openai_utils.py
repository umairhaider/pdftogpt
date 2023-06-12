import pytest
from unittest.mock import patch, MagicMock
from app.utils import openai_utils

def test_generate_chatgpt_response_exception():
    """
    Test that generate_chatgpt_response function raises an exception
    when the OpenAI API call fails.
    """
    with patch('os.getenv', return_value='testkey'):
        # Mock OpenAI API call to raise an exception
        with patch("openai.ChatCompletion.create", side_effect=Exception("Unexpected error")):
            with pytest.raises(Exception) as e_info:
                openai_utils.generate_chatgpt_response("test text")
            assert str(e_info.value) == "Unexpected error"
