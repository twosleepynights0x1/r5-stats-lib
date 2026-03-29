"""Основной клиент для работы с Apex Legends API"""

import os
import time
import logging
from typing import Optional, Dict, Any, List, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .errors import (
    ApexAPIError,
    PlayerNotFoundError,
    RateLimitError,
    InvalidAPIKeyError,
    APIError,
    ValidationError
)
from .models import PlayerStats, MapInfo, MapRotation, PredatorInfo, ServerStatus
from .endpoints.player import PlayerEndpoint
from .endpoints.map_rotation import MapRotationEndpoint
from .endpoints.predator import PredatorEndpoint
from .endpoints.servers import ServersEndpoint
from .utils.rate_limiter import RateLimiter
from .utils.validators import validate_platform, validate_player_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApexClient:
    """Основной клиент для Apex Legends API"""

    BASE_URL = "https://api.mozambiquehe.re"

    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit_delay: float = 2.0,
        timeout: int = 10,
        max_retries: int = 3,
        debug: bool = False
    ):
        """Инициализация клиента"""
        self.api_key = api_key or os.getenv("APEX_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not found! Provide it explicitly or set APEX_API_KEY environment variable"
            )

        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        self.debug = debug
        self.rate_limiter = RateLimiter(min_interval=rate_limit_delay)
        self.session = self._create_session(max_retries)
        self.session.headers.update({
            "Authorization": self.api_key,
            "User-Agent": "ApexLegendsPy/1.0.0"
        })

        # Initialize endpoints
        self.player = PlayerEndpoint(self)
        self.map_rotation = MapRotationEndpoint(self)
        self.predator = PredatorEndpoint(self)
        self.servers = ServersEndpoint(self)

        if debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("ApexClient initialized in debug mode")

    def _create_session(self, max_retries: int) -> requests.Session:
        """Creates session with retry settings"""
        session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        ignore_rate_limit: bool = False
    ) -> Dict[str, Any]:
        """Internal method for making requests"""
        url = f"{self.BASE_URL}/{endpoint}"
        params = params or {}
        
        if "auth" not in params:
            params["auth"] = self.api_key

        if not ignore_rate_limit:
            self.rate_limiter.wait_if_needed()

        start_time = time.time()

        try:
            if self.debug:
                logger.debug(f"Request: GET {url}")
                logger.debug(f"Params: {params}")

            response = self.session.get(url, params=params, timeout=self.timeout)
            response_time = (time.time() - start_time) * 1000

            if self.debug:
                logger.debug(f"Response: {response.status_code} ({response_time:.0f}ms)")

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                raise InvalidAPIKeyError()
            elif response.status_code == 404:
                player_name = params.get("player", "unknown")
                platform = params.get("platform", "unknown")
                raise PlayerNotFoundError(player_name, platform)
            elif response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                raise RateLimitError(int(retry_after) if retry_after else None)
            elif response.status_code == 400:
                raise APIError(f"Bad request: {response.text}")
            elif response.status_code == 410:
                raise ValidationError("Invalid platform. Available: PC, PS4, X1, SWITCH")
            else:
                raise APIError(f"API error (code {response.status_code}): {response.text}")

        except requests.exceptions.Timeout:
            raise APIError("Connection timeout. API is not responding.")
        except requests.exceptions.ConnectionError:
            raise APIError("Connection error. Check your internet.")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request error: {str(e)}")

    def get_player(
        self,
        name: Optional[str] = None,
        uid: Optional[str] = None,
        platform: str = "PC",
        **kwargs
    ) -> PlayerStats:
        """Get player statistics"""
        if not name and not uid:
            raise ValidationError("Provide either name or uid")

        if name:
            validate_player_name(name)

        platform = validate_platform(platform)

        params = {
            "platform": platform,
            "version": kwargs.get("version", 5)
        }

        if name:
            params["player"] = name
        else:
            params["uid"] = uid

        if kwargs.get("merge"):
            params["merge"] = "true"
        if kwargs.get("skip_rank"):
            params["skipRank"] = "true"

        data = self._request("bridge", params)
        return self.player._parse_response(data, name or "unknown", platform)

    def get_current_map(self) -> str:
        """Get current map name"""
        rotation = self.get_map_rotation()
        return rotation.get("battle_royale", {}).current.name if rotation.get("battle_royale") else "Unknown"

    def get_map_rotation(self, version: str = "2") -> Dict[str, MapRotation]:
        """Get full map rotation"""
        data = self._request("maprotation", {"version": version})
        return self.map_rotation._parse_response(data)

    def get_predator_info(self) -> List[PredatorInfo]:
        """Get predator information"""
        data = self._request("predator")
        return self.predator._parse_response(data)

    def get_server_status(self) -> List[ServerStatus]:
        """Get server status"""
        data = self._request("servers")
        return self.servers._parse_response(data)

    def close(self):
        """Close session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()