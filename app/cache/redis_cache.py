# General Imports
import redis
from typing import Union

# Package Imports
from app.core import app_config

redis_client = redis.StrictRedis.from_url(app_config.redis_url, decode_responses=True)

def get_cached_response(key: str)-> Union[str, None]:
    """Get a cached response from Redis"""
    value = redis_client.get(key)
    return value if value else None

def set_cached_response(key: str, value: str)-> None:
    """Set a cached response in Redis"""
    redis_client.set(key, value)
