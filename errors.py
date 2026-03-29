"""Кастомные исключения для библиотеки"""


class ApexAPIError(Exception):
    """Базовое исключение для всех ошибок API"""
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message)


class PlayerNotFoundError(ApexAPIError):
    """Игрок не найден"""
    def __init__(self, player_name: str, platform: str):
        self.player_name = player_name
        self.platform = platform
        super().__init__(f"❌ Игрок '{player_name}' не найден на платформе '{platform}'")


class RateLimitError(ApexAPIError):
    """Превышен лимит запросов"""
    def __init__(self, retry_after: int = None):
        self.retry_after = retry_after
        message = "❌ Превышен лимит запросов. Подождите немного."
        if retry_after:
            message += f" Повторите через {retry_after} секунд."
        super().__init__(message)


class InvalidAPIKeyError(ApexAPIError):
    """Неверный API ключ"""
    def __init__(self):
        super().__init__("❌ Неверный API ключ. Проверьте ваш ключ на https://portal.apexlegendsapi.com/")


class APIError(ApexAPIError):
    """Общая ошибка API"""
    pass


class ValidationError(ApexAPIError):
    """Ошибка валидации параметров"""
    pass