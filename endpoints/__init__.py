"""Эндпоинты API"""

from .player import PlayerEndpoint
from .map_rotation import MapRotationEndpoint
from .predator import PredatorEndpoint
from .servers import ServersEndpoint

__all__ = [
    "PlayerEndpoint",
    "MapRotationEndpoint", 
    "PredatorEndpoint",
    "ServersEndpoint"
]