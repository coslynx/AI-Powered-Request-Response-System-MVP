from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

from ..database import get_db, SessionLocal
from ..models import Request, Response
from ..utils import openai_api_call

router = APIRouter()

class RequestSchema(BaseModel):
    text: str = Field(..., description="The text to process.")
    model: Optional[str] = Field(
        "text-davinci-003",
        description="The OpenAI model to use (defaults to text-davinci-003).",
    )
    max_tokens: Optional[int] = Field(
        1024,
        description="The maximum number of tokens to generate (defaults to 1024).",
    )

class ResponseSchema(BaseModel):
    response: str = Field(..., description="The AI-generated response.")

@router.post("/", response_model=ResponseSchema)
async def process_request(request: RequestSchema, db: SessionLocal = Depends(get_db)):
    try:
        response_text = await openai_api_call(
            prompt=request.text, model=request.model, max_tokens=request.max_tokens
        )

        new_response = Response(text=response_text, request_id=request.id)
        db.add(new_response)
        db.commit()
        db.refresh(new_response)

        return ResponseSchema(response=response_text)

    except openai.error.APIError as e:
        raise HTTPException(
            status_code=500, detail=f"OpenAI API Error: {e}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")