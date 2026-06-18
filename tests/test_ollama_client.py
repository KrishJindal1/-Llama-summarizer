from unittest.mock import patch

from core.ollama_client import chat

@patch("core.ollama_client.ollama.chat")
def test_chat(mock_chat):

    mock_chat.return_value = {
        "message": {
            "content": "Hello"
        }
    }

    result = chat(
        model="llama3",
        messages=[]
    )

    assert result["message"]["content"] == "Hello"