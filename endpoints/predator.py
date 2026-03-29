"""Эндпоинт для информации о предаторе"""

from typing import List, Dict, Any
from ..models import PredatorInfo


class PredatorEndpoint:
    """Обработчик запросов к /predator эндпоинту"""
    
    def __init__(self, client):
        self.client = client
    
    def _parse_response(self, data: Dict[str, Any]) -> List[PredatorInfo]:
        """Парсит JSON ответ в список PredatorInfo"""
        predators = []
        
        # Данные находятся внутри ключа "RP"
        rp_data = data.get("RP", {})
        
        platform_mapping = {
            "PC": "PC",
            "PS4": "PlayStation",
            "X1": "Xbox",
            "SWITCH": "Nintendo Switch"
        }
        
        for platform, info in rp_data.items():
            predators.append(PredatorInfo(
                platform=platform_mapping.get(platform, platform),
                required_rp=info.get("val", 0),
                masters_count=info.get("totalMastersAndPreds", 0),
                predator_count=info.get("foundRank", 0)
            ))
        
        return predators