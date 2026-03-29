"""Модели данных для ответов API"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class PlayerStats:
    """Статистика игрока"""
    name: str
    uid: str
    platform: str
    level: int
    prestige: int
    kills: int
    deaths: int
    wins: int
    rank_name: str
    rank_score: int
    rank_division: int
    rank_image: Optional[str] = None
    current_legend: str = "Unknown"
    current_legend_kills: int = 0
    games_played: int = 0
    kills_by_legend: Dict[str, int] = field(default_factory=dict)
    
    @property
    def kd_ratio(self) -> float:
        if self.deaths > 0:
            return round(self.kills / self.deaths, 2)
        return float(self.kills)
    
    @property
    def total_level(self) -> int:
        return self.prestige * 500 + self.level
    
    def __repr__(self) -> str:
        return f"<PlayerStats: {self.name} (Prestige {self.prestige} Level {self.level}) | {self.kills} kills>"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "uid": self.uid,
            "platform": self.platform,
            "level": self.level,
            "prestige": self.prestige,
            "total_level": self.total_level,
            "kills": self.kills,
            "deaths": self.deaths,
            "wins": self.wins,
            "kd_ratio": self.kd_ratio,
            "rank": self.rank_name,
            "rank_score": self.rank_score,
            "current_legend": self.current_legend,
            "current_legend_kills": self.current_legend_kills,
            "games_played": self.games_played
        }


@dataclass
class MapInfo:
    """Информация о карте"""
    name: str
    image_url: str
    remaining_seconds: int
    remaining_timer: str
    is_ranked: bool = False
    
    @property
    def remaining_minutes(self) -> int:
        return self.remaining_seconds // 60
    
    @property
    def remaining_formatted(self) -> str:
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        return f"{minutes}:{seconds:02d}"


@dataclass
class MapRotation:
    """Ротация карт"""
    current: MapInfo
    next: MapInfo
    mode: str


@dataclass
class PredatorInfo:
    """Информация о предаторе"""
    platform: str
    required_rp: int
    masters_count: int
    predator_count: int
    
    def __repr__(self) -> str:
        return f"<Predator {self.platform}: {self.required_rp} RP>"


@dataclass
class ServerStatus:
    """Статус серверов"""
    platform: str
    status: str
    response_time: int
    last_checked: datetime
    
    @property
    def is_online(self) -> bool:
        return self.status == "ONLINE"