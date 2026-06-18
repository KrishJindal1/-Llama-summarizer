from unittest.mock import patch
from core.analyzer import (generate_summary, rewrite_content)


@patch("core.analyzer.chat")
def test_generate_summary(mock_chat):

    mock_chat.return_value = {
        "message": {
            "content": "Test Summary"
        }
    }

    result = generate_summary(
        "Hello World",
        "Short",
        "llama3"
    )

    assert result == "Test Summary"

@patch("core.analyzer.chat")
def test_rewrite_content(mock_chat):

    mock_chat.return_value = {
        "message": {
            "content": "Rewritten Text"
        }
    }

    result = rewrite_content(
        "Original Text",
        "Summary",
        "Professional",
        0.5,
        "Summary",
        "llama3"
    )

    assert result == "Rewritten Text"