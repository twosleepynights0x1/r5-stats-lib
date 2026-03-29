"""Эндпоинт для работы со статистикой игроков"""

from typing import Dict, Any
from ..models import PlayerStats


class PlayerEndpoint:
    """Обработчик запросов к /bridge эндпоинту"""
    
    def __init__(self, client):
        self.client = client
    
    def _parse_response(self, data: Dict[str, Any], player_name: str, platform: str) -> PlayerStats:
        """Парсит JSON ответ в объект PlayerStats"""
        try:
            global_stats = data.get("global", {})
            rank_info = global_stats.get("rank", {})
            total_stats = data.get("total", {})
            realtime = data.get("realtime", {})
            legends_data = data.get("legends", {})
            
            uid = data.get("uid", "")
            if not uid:
                uid = global_stats.get("uid", "")
            
            current_legend = realtime.get("selectedLegend", "Unknown")
            
            current_legend_kills = 0
            kills_by_legend = {}
            
            all_legends = legends_data.get("all", {})
            for legend_name, legend_info in all_legends.items():
                for stat in legend_info.get("data", []):
                    if stat.get("key") == "kills":
                        kills = stat.get("value", 0)
                        if isinstance(kills, str):
                            try:
                                kills = int(kills)
                            except ValueError:
                                kills = 0
                        if kills > 0:
                            kills_by_legend[legend_name] = kills
                            if legend_name == current_legend:
                                current_legend_kills = kills
            
            if current_legend_kills == 0 and current_legend != "Unknown":
                selected = legends_data.get("selected", {})
                for stat in selected.get("data", []):
                    if stat.get("key") == "kills":
                        kills = stat.get("value", 0)
                        if isinstance(kills, str):
                            try:
                                kills = int(kills)
                            except ValueError:
                                kills = 0
                        current_legend_kills = kills
            
            kills = 0
            kills_data = total_stats.get("kills", {})
            if isinstance(kills_data, dict):
                kills_value = kills_data.get("value", 0)
                if isinstance(kills_value, str):
                    try:
                        kills = int(kills_value)
                    except ValueError:
                        kills = 0
                else:
                    kills = kills_value
            
            if kills == 0:
                kills = sum(kills_by_legend.values())
            
            wins = 0
            wins_data = total_stats.get("wins", {})
            if isinstance(wins_data, dict):
                wins_value = wins_data.get("value", 0)
                if isinstance(wins_value, str):
                    try:
                        wins = int(wins_value)
                    except ValueError:
                        wins = 0
                else:
                    wins = wins_value
            
            if wins == 0:
                special_wins = total_stats.get("specialEvent_wins", {})
                if isinstance(special_wins, dict):
                    wins_value = special_wins.get("value", 0)
                    if isinstance(wins_value, str):
                        try:
                            wins = int(wins_value)
                        except ValueError:
                            wins = 0
                    else:
                        wins = wins_value
            
            deaths = 0
            kd_data = total_stats.get("kd", {})
            if isinstance(kd_data, dict):
                kd_value = kd_data.get("value", -1)
                if isinstance(kd_value, str):
                    try:
                        kd_value = float(kd_value)
                    except ValueError:
                        kd_value = -1
                if kd_value != -1 and kd_value > 0 and kills > 0:
                    deaths = int(kills / kd_value)
            
            prestige = global_stats.get("levelPrestige", 0)
            if isinstance(prestige, str):
                try:
                    prestige = int(prestige)
                except ValueError:
                    prestige = 0
            
            level = global_stats.get("level", 0)
            if isinstance(level, str):
                try:
                    level = int(level)
                except ValueError:
                    level = 0
            
            rank_score = rank_info.get("rankScore", 0)
            if isinstance(rank_score, str):
                try:
                    rank_score = int(rank_score)
                except ValueError:
                    rank_score = 0
            
            rank_division = rank_info.get("rankDiv", 0)
            if isinstance(rank_division, str):
                try:
                    rank_division = int(rank_division)
                except ValueError:
                    rank_division = 0
            
            games_played = global_stats.get("internalUpdateCount", 0)
            if isinstance(games_played, str):
                try:
                    games_played = int(games_played)
                except ValueError:
                    games_played = 0
            
            return PlayerStats(
                name=global_stats.get("name", player_name),
                uid=uid,
                platform=platform,
                level=level,
                prestige=prestige,
                kills=kills,
                deaths=deaths,
                wins=wins,
                rank_name=rank_info.get("rankName", "Unranked"),
                rank_score=rank_score,
                rank_division=rank_division,
                rank_image=rank_info.get("rankImg"),
                current_legend=current_legend,
                current_legend_kills=current_legend_kills,
                games_played=games_played,
                kills_by_legend=kills_by_legend
            )
        except Exception as e:
            if hasattr(self.client, 'logger'):
                self.client.logger.error(f"Error parsing response: {e}")
            raise Exception(f"Failed to parse API response: {e}")