from typing import Dict, Any
import jwt
from fastapi import HTTPException
import logging
from datetime import datetime, timedelta
import requests
import cachetools

# Initialize logging
logger = logging.getLogger(__name__)

# Define constants
JWT_SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with your actual secret key
CACHE_MAXSIZE = 1024  # Set the maximum size of the cache
CACHE_TTL = 3600  # Set the cache time-to-live in seconds (1 hour)

# Define a cache using the LRU (Least Recently Used) strategy
cache = cachetools.LRUCache(maxsize=CACHE_MAXSIZE)

# Function to generate a JWT token
def generate_jwt_token(user_id: int, role: str) -> str:
    """Generates a JWT token for the given user ID and role.

    Args:
        user_id: The ID of the user.
        role: The role of the user.

    Returns:
        A JWT token.
    """
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=30),  # Set token expiration time
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token

# Function to verify a JWT token
def verify_jwt_token(token: str) -> Dict[str, Any]:
    """Verifies the given JWT token and extracts the payload.

    Args:
        token: The JWT token to verify.

    Returns:
        The decoded token payload if the token is valid.

    Raises:
        HTTPException: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("JWT token has expired.")
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        logger.error("Invalid JWT token.")
        raise HTTPException(status_code=401, detail="Invalid token.")

# Function to make a cached API call
def cached_api_call(url: str, method: str = "GET", data: Dict[str, Any] = None) -> Any:
    """Makes a cached API call to the given URL.

    Args:
        url: The URL of the API endpoint.
        method: The HTTP method to use (default: "GET").
        data: The data to send in the request body (optional).

    Returns:
        The response data from the API.

    Raises:
        HTTPException: If there is an error making the API call.
    """
    key = f"{method}:{url}:{data}"  # Generate a unique cache key
    cached_response = cache.get(key)

    if cached_response is not None:
        logger.info(f"Returning cached response for {key}")
        return cached_response

    try:
        response = requests.request(method=method, url=url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Cache the response if successful
        cache[key] = response.json()
        logger.info(f"Caching response for {key}")

        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        raise HTTPException(status_code=500, detail=f"API call failed: {e}")

# Function to handle API errors
def handle_api_error(response: requests.Response) -> None:
    """Handles errors returned from an API call.

    Args:
        response: The API response.

    Raises:
        HTTPException: If the API call failed.
    """
    if response.status_code >= 400:
        try:
            error_data = response.json()
            error_message = error_data.get("message")
            logger.error(f"API error: {error_message}")
            raise HTTPException(status_code=response.status_code, detail=error_message)
        except ValueError:
            logger.error(f"API error: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)