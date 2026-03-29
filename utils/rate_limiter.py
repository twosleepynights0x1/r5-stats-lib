"""Rate limiter для соблюдения ограничений API"""

import time
import threading
from typing import Optional


class RateLimiter:
    """Простой rate limiter для контроля частоты запросов"""
    
    def __init__(self, min_interval: float = 2.0):
        """
        Args:
            min_interval: Минимальный интервал между запросами в секундах
        """
        self.min_interval = min_interval
        self.last_request_time: Optional[float] = None
        self._lock = threading.Lock()
    
    def wait_if_needed(self) -> None:
        """Ожидает, если нужно соблюсти rate limit"""
        with self._lock:
            if self.last_request_time is not None:
                elapsed = time.time() - self.last_request_time
                if elapsed < self.min_interval:
                    wait_time = self.min_interval - elapsed
                    time.sleep(wait_time)
            
            self.last_request_time = time.time()
    
    def reset(self) -> None:
        """Сбрасывает rate limiter"""
        with self._lock:
            self.last_request_time = None