"""
Apex Legends API Wrapper - Simple library for Apex Legends API
"""

__version__ = "0.0.4"
__author__ = "Your Name"

from .client import ApexClient
from .models import PlayerStats, MapInfo, MapRotation, PredatorInfo, ServerStatus
from .errors import ApexAPIError, PlayerNotFoundError, RateLimitError, InvalidAPIKeyError, APIError, ValidationError

__all__ = [
    "ApexClient",
    "PlayerStats",
    "MapInfo",
    "MapRotation",
    "PredatorInfo",
    "ServerStatus",
    "ApexAPIError",
    "PlayerNotFoundError",
    "RateLimitError",
    "InvalidAPIKeyError",
    "APIError",
    "ValidationError"
]