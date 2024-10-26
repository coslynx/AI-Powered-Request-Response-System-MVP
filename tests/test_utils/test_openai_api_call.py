import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from utils.openai_api_call import openai_api_call

from main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_openai_api_call_success():
    """Tests a successful API call with a valid prompt."""
    with patch('openai.Completion.create') as mock_create:
        mock_create.return_value = {
            "choices": [
                {"text": "This is a test response."}
            ]
        }
        response = await openai_api_call(prompt="Test prompt", model="text-davinci-003", max_tokens=1024)
        assert response == "This is a test response."

@pytest.mark.asyncio
async def test_openai_api_call_error():
    """Tests handling of API errors."""
    with patch('openai.Completion.create') as mock_create:
        mock_create.side_effect = openai.error.APIError("Test error")
        with pytest.raises(Exception) as e:
            await openai_api_call(prompt="Test prompt", model="text-davinci-003", max_tokens=1024)
        assert "Test error" in str(e)

@pytest.mark.asyncio
async def test_openai_api_call_rate_limit():
    """Tests handling of API rate limit errors."""
    with patch('openai.Completion.create') as mock_create:
        mock_create.side_effect = openai.error.RateLimitError("Rate limit exceeded")
        with pytest.raises(Exception) as e:
            await openai_api_call(prompt="Test prompt", model="text-davinci-003", max_tokens=1024)
        assert "Rate limit exceeded" in str(e)

@pytest.mark.asyncio
async def test_openai_api_call_openai_error():
    """Tests handling of generic OpenAI errors."""
    with patch('openai.Completion.create') as mock_create:
        mock_create.side_effect = openai.error.OpenAIError("General OpenAI error")
        with pytest.raises(Exception) as e:
            await openai_api_call(prompt="Test prompt", model="text-davinci-003", max_tokens=1024)
        assert "General OpenAI error" in str(e)