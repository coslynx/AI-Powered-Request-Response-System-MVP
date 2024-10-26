import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Optional

from pydantic import BaseModel, Field

from ..database import get_db, SessionLocal
from ..models import Request, Response

from ..utils import openai_api_call
from routers.process import router, RequestSchema, ResponseSchema

# Mock OpenAI API response for testing
mock_response = {
    "choices": [
        {
            "text": "This is a mock response from OpenAI API.",
        }
    ]
}

# Mock the openai_api_call function
@pytest.fixture
def mock_openai_api_call(monkeypatch):
    async def _mock_openai_api_call(*args, **kwargs):
        return mock_response

    monkeypatch.setattr("routers.process.openai_api_call", _mock_openai_api_call)


# Mock the database session
@pytest.fixture
def mock_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test the process_request function
def test_process_request(mock_openai_api_call, mock_db):
    client = TestClient(router)

    # Create a test request
    test_request = RequestSchema(
        text="This is a test request.",
        model="text-davinci-003",
        max_tokens=1024,
    )

    # Send the request to the API
    response = client.post("/", json=test_request.dict())

    # Assert the status code
    assert response.status_code == 200

    # Assert the response content
    assert response.json() == {"response": "This is a mock response from OpenAI API."}

    # Assert the request was saved to the database
    assert mock_db.query(Response).filter(Response.request_id == 1).first() is not None

    # Assert the request was saved to the database
    assert mock_db.query(Request).filter(Request.id == 1).first() is not None