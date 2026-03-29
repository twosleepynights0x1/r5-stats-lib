"""Эндпоинт для статуса серверов"""

from typing import List, Dict, Any
from datetime import datetime
from ..models import ServerStatus


class ServersEndpoint:
    """Обработчик запросов к /servers эндпоинту"""
    
    def __init__(self, client):
        self.client = client
    
    def _parse_response(self, data: Dict[str, Any]) -> List[ServerStatus]:
        """Парсит JSON ответ в список ServerStatus"""
        servers = []
        
        for platform, info in data.items():
            servers.append(ServerStatus(
                platform=platform.upper(),
                status=info.get("Status", "UNKNOWN"),
                response_time=info.get("ResponseTime", 0),
                last_checked=datetime.now()
            ))
        
        return servers