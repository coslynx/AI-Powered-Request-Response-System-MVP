from typing import Optional
import openai
import requests
import cachetools
from . import settings  # Import settings from the `config.py` file.
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

# Define a cache using the LRU (Least Recently Used) strategy.
cache = cachetools.LRUCache(maxsize=1024)

# Set the OpenAI API key from the settings object.
openai.api_key = settings.API_KEY


async def openai_api_call(
    prompt: str, model: Optional[str] = None, max_tokens: int = 1024
) -> str:
    """
    Makes a request to the OpenAI API to generate text.

    Args:
        prompt: The text prompt to use for generating text.
        model: The OpenAI model to use. Defaults to the `MODEL` setting from `config.py`.
        max_tokens: The maximum number of tokens to generate. Defaults to 1024.

    Returns:
        The generated text from the OpenAI API.

    Raises:
        HTTPException: If there is an error making the API call.
    """
    key = f"{prompt}:{model}:{max_tokens}"  # Generate a unique cache key.
    cached_response = cache.get(key)
    if cached_response is not None:
        logger.info(f"Returning cached response for {key}")
        return cached_response
    try:
        response = await openai.Completion.create(
            engine=model or settings.MODEL,
            prompt=prompt,
            max_tokens=max_tokens,
        )
        response_text = response.choices[0].text
        cache[key] = response_text  # Cache the response if successful.
        logger.info(f"Caching response for {key}")
        return response_text
    except openai.error.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    except openai.error.RateLimitError as e:
        logger.error(f"OpenAI rate limit error: {e}")
        raise HTTPException(status_code=429, detail=f"OpenAI rate limit error: {e}")
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")