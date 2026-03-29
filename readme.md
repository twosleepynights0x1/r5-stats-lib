## Установка
```pip
pip install r5-stat
```
---

## Инициализация клиента
```python
from apex_legends_py import ApexClient

# Способ 1: Через переменную окружения (нужно установить APEX_API_KEY)
client = ApexClient()

# Способ 2: Прямая передача ключа
client = ApexClient(api_key="YOUR_API_KEY")

# Способ 3: С пользовательскими настройками
client = ApexClient(
    api_key="YOUR_API_KEY",
    rate_limit_delay=2.0,
    timeout=10,
    max_retries=3,
    debug=False
)

# Способ 4: Через контекстный менеджер
with ApexClient(api_key="YOUR_API_KEY") as client:
    player = client.get_player("ImperialHal")
```
---

## Пример получения игрока
```python
# По имени (платформа по умолчанию PC)
player = client.get_player("ImperialHal")

# По имени и платформе
player = client.get_player(name="ImperialHal", platform="PC")

# По UID (требуется указать платформу)
player = client.get_player(uid="2796574388", platform="PC")

# По UID и платформе
player = client.get_player(uid="2796574388", platform="PC")
```

Доступные платформы: `PC`, `PS4`, `X1`, `SWITCH`
---


## Основные типы информации

| Поле | Тип | Описание | Пример получения |
|------|-----|----------|------------------|
| `name` | `str` | Имя игрока | `player.name` |
| `uid` | `str` | Уникальный ID игрока | `player.uid` |
| `platform` | `str` | Платформа (PC, PS4, X1, SWITCH) | `player.platform` |

## Уровень и престиж

| Поле | Тип | Описание | Пример получения |
|------|-----|----------|------------------|
| `level` | `int` | Текущий уровень (1-500) | `player.level` |
| `prestige` | `int` | Престиж (0-4) | `player.prestige` |
| `total_level` | `int` | Полный уровень (prestige * 500 + level) | `player.total_level` |

## Боевая статистика

| Поле | Тип | Описание | Пример получения |
|------|-----|----------|------------------|
| `kills` | `int` | Всего убийств | `player.kills` |
| `deaths` | `int` | Всего смертей | `player.deaths` |
| `wins` | `int` | Всего побед | `player.wins` |
| `kd_ratio` | `float` | Соотношение убийств к смертям | `player.kd_ratio` |
| `games_played` | `int` | Всего сыграно игр | `player.games_played` |

## Ранговые данные

| Поле | Тип | Описание | Пример получения |
|------|-----|----------|------------------|
| `rank_name` | `str` | Название ранга | `player.rank_name` |
| `rank_score` | `int` | Ранговые очки (RP) | `player.rank_score` |
| `rank_division` | `int` | Дивизион ранга | `player.rank_division` |
| `rank_image` | `str` | URL изображения ранга | `player.rank_image` |

### Возможные значения rank_name
- `Unranked`
- `Bronze`
- `Silver`
- `Gold`
- `Platinum`
- `Diamond`
- `Master`
- `Apex Predator`

## Текущая легенда

| Поле | Тип | Описание | Пример получения |
|------|-----|----------|------------------|
| `current_legend` | `str` | Имя текущей легенды | `player.current_legend` |
| `current_legend_kills` | `int` | Убийств на текущей легенде | `player.current_legend_kills` |

## Убийства по всем легендам

| Поле | Тип | Описание | Пример получения |
|------|-----|----------|------------------|
| `kills_by_legend` | `dict` | Словарь {легенда: убийства} | `player.kills_by_legend` |

## Методы

| Метод | Возвращает | Описание | Пример получения |
|-------|-----------|----------|------------------|
| `to_dict()` | `dict` | Конвертирует все данные в словарь | `player.to_dict()` |

## Пример получения всех данных

```python
from apex_legends_py import ApexClient

client = ApexClient(api_key="YOUR_API_KEY")
player = client.get_player("ImperialHal")

# Основная информация
print(player.name)
print(player.uid)
print(player.platform)

# Уровень и престиж
print(player.level)
print(player.prestige)
print(player.total_level)

# Боевая статистика
print(player.kills)
print(player.deaths)
print(player.wins)
print(player.kd_ratio)
print(player.games_played)

# Ранговые данные
print(player.rank_name)
print(player.rank_score)
print(player.rank_division)
print(player.rank_image)

# Текущая легенда
print(player.current_legend)
print(player.current_legend_kills)

# Убийства по легендам
for legend, kills in player.kills_by_legend.items():
    print(f"{legend}: {kills}")

# Конвертация в словарь
data = player.to_dict()
print(data)
```

---
## Другие мтоды клиента
```python
get_current_map()
Описание: Возвращает название текущей карты в Battle Royale
Возвращает: str
Пример: current_map = client.get_current_map()
```
```pytohn
get_map_rotation()
Описание: Возвращает полную ротацию карт для всех режимов
Возвращает: dict с ключами battle_royale, arenas, control
Пример: rotation = client.get_map_rotation()
```
```python
get_predator_info()
Описание: Возвращает информацию о порогах Apex Predator на всех платформах
Возвращает: List[PredatorInfo]
Пример: predators = client.get_predator_info()
```
```python
get_server_status()
Описание: Возвращает статус серверов EA
Возвращает: List[ServerStatus]
Пример: servers = client.get_server_status()
```


---

## Данные мап-ротаций

### `Метод get_map_rotation() возвращает словарь:`
```python
rotation = client.get_map_rotation()

# Battle Royale режим
br = rotation.get("battle_royale")
br.current.name              # Текущая карта
br.current.remaining_seconds # Осталось секунд
br.current.remaining_timer   # Осталось времени в формате MM:SS
br.current.remaining_minutes # Осталось минут
br.current.remaining_formatted # Отформатированное время
br.next.name                 # Следующая карта

# Arenas режим
arenas = rotation.get("arenas")
arenas.current.name
arenas.next.name

# Control режим
control = rotation.get("control")
control.current.name
control.next.name
```


---

## Данные о предаторах


### `Метод get_predator_info() возвращает список объектов PredatorInfo:`

```python
predators = client.get_predator_info()

for pred in predators:
    pred.platform        # Название платформы (PC, PlayStation, Xbox, Nintendo Switch)
    pred.required_rp     # Количество RP необходимое для достижения Predator
    pred.masters_count   # Количество игроков в ранге Master
    pred.predator_count  # Количество игроков в ранге Predator
```


---

## Сервер статус

### `Метод get_server_status() возвращает список объектов ServerStatus:`


```python
servers = client.get_server_status()

for server in servers:
    server.platform      # Название сервера
    server.status        # Статус (ONLINE или OFFLINE)
    server.response_time # Время ответа в миллисекундах
    server.is_online     # True если сервер онлайн, False если оффлайн
```

---

## Обработка ошибок

```python
from apex_legends_py import (
    ApexClient,
    PlayerNotFoundError,
    InvalidAPIKeyError,
    RateLimitError,
    ValidationError,
    APIError
)

client = ApexClient(api_key="YOUR_API_KEY")

try:
    player = client.get_player("NonexistentPlayer")
except PlayerNotFoundError as e:
    print(f"Игрок не найден: {e}")
except InvalidAPIKeyError as e:
    print(f"Неверный API ключ: {e}")
except RateLimitError as e:
    print(f"Превышен лимит запросов: {e}")
except ValidationError as e:
    print(f"Неверный параметр: {e}")
except APIError as e:
    print(f"Ошибка API: {e}")
```



## Как получить апи ключь

API ключ можно получить на сайте:
https://portal.apexlegendsapi.com/


---

## Доступные платформы

* PC     - Компьютеры (Origin/Steam)
* PS4    - PlayStation 4/5
* X1     - Xbox One/Series
* SWITCH - Nintendo Switch

---

## Лимиты запросов

По умолчанию: 1 запрос в 2 секунды
После подключения Discord аккаунта: 2 запроса в секунду

Библиотека автоматически соблюдает лимиты.
