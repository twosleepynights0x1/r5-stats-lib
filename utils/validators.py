"""Валидаторы для входных параметров"""

from typing import Optional
from ..errors import ValidationError

VALID_PLATFORMS = ["PC", "PS4", "X1", "SWITCH"]


def validate_platform(platform: str) -> str:
    """
    Валидирует и нормализует платформу
    
    Args:
        platform: Название платформы
    
    Returns:
        Нормализованное название платформы
    """
    platform = platform.upper().strip()
    
    # Синонимы
    synonyms = {
        "PC": "PC",
        "ORIGIN": "PC",
        "STEAM": "PC",
        "PLAYSTATION": "PS4",
        "PS": "PS4",
        "PS5": "PS4",
        "XBOX": "X1",
        "XB": "X1",
        "XBOXONE": "X1",
        "NINTENDO": "SWITCH",
        "SW": "SWITCH"
    }
    
    if platform in synonyms:
        return synonyms[platform]
    
    if platform not in VALID_PLATFORMS:
        raise ValidationError(
            f"❌ Неверная платформа: '{platform}'. "
            f"Доступные: {', '.join(VALID_PLATFORMS)}"
        )
    
    return platform


def validate_player_name(name: str) -> None:
    """
    Валидирует имя игрока
    
    Args:
        name: Имя игрока
    """
    if not name or not isinstance(name, str):
        raise ValidationError("❌ Имя игрока должно быть непустой строкой")
    
    if len(name) > 50:
        raise ValidationError("❌ Имя игрока не может быть длиннее 50 символов")
    
    # Имена Apex могут содержать буквы, цифры, некоторые спецсимволы
    # Пропускаем базовую валидацию