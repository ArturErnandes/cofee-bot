# Command API

Актуальная спецификация HTTP API модуля `python/server.py`.

- Framework: FastAPI
- Entry point: `python/server.py`
- Модель данных: `python/classes.py` (`Command`)

---

## 1. Endpoint

Base URL (локально): `http://localhost:8080`

| Endpoint | Method | Назначение |
|---|---|---|
| `/command` | `POST` | Принять команду и вернуть подтверждение |

Декоратор:
- `tags=["Команды"]`
- `summary="Передача новой команды серверу"`

---

## 2. Входной контракт

Обработчик:

```python
def put_command(command: str, time: float):
```

Параметры принимаются как query-параметры:

| Параметр | Тип | Обязательность | Пример |
|---|---|---|---|
| `command` | `string` | да | `forward` |
| `time` | `float` | да | `1.5` |

Пример запроса:

```bash
curl -X POST "http://localhost:8080/command?command=forward&time=1.5"
```

---

## 3. Выходной контракт

При успешной обработке возвращается `200 OK`:

```json
{
  "message": "Command 'forward' executed successfully"
}
```

Формат поля:
- `message: string`

---

## 4. Внутренняя обработка

1. Из входных параметров создаётся объект `Command`:
   - `message=command`
   - `time=time`
2. Объект используется локально в handler.
3. Возвращается строка-подтверждение.

---

## 5. Ограничения текущей реализации

1. Endpoint не проксирует команду в C++ контур (`engine_controll`) и не вызывает реальный исполнительный движок.
2. Нет очереди команд, статуса выполнения и idempotency-механизма.
3. Нет бизнес-валидации допустимых команд (`forward/right/left/stop`) и ограничений по времени.
4. Нет авторизации/аутентификации.

---

## 6. Ошибки валидации (FastAPI/Pydantic)

Примеры:

- отсутствует `command` или `time` -> `422 Unprocessable Entity`
- `time` не приводится к `float` -> `422 Unprocessable Entity`

Пример некорректного запроса:

```bash
curl -X POST "http://localhost:8080/command?command=forward&time=abc"
```

---

## 7. Планируемый целевой контракт (рекомендация)

Для следующего этапа интеграции обычно добавляют:

1. JSON body (`{"command":"forward","duration_ms":1000}`) вместо query.
2. Явный enum команд.
3. Асинхронную постановку в очередь и endpoint статуса (`/commands/{id}`).
4. Связь с navigation-выходом (`distance/angle` -> команда движения).
