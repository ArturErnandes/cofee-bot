# Future Tasks

План развития интеграции контейнеров `vision`, `api`, `control` и добавления RabbitMQ.

---

## 1. Текущее состояние (skeleton)

- Контейнеры `vision`, `api`, `control` запускаются через `docker-compose.yml`.
- Межмодульная связь пока не реализована.
- `vision` уже получает `API_BASE_URL` через env как подготовку к HTTP интеграции.

---

## 2. Этап A — связь `vision -> api` (HTTP)

### Цель

Передавать команды от vision в API синхронно.

### Задачи

1. В `vision` добавить клиент API (`requests`/`httpx`) для `POST /command`.
2. Ввести нормализованный payload (например, `command`, `duration_ms`, `request_id`).
3. Добавить таймауты и retry-политику на стороне `vision`.
4. Добавить логирование correlation id (`request_id`) в `vision` и `api`.

### Критерии готовности

- Команда, сгенерированная в vision, появляется в логах API.
- В случае недоступности API vision не падает, а повторяет отправку по политике retry.

---

## 3. Этап B — RabbitMQ между `api` и `control`

### Цель

Отвязать `api` от `control` и ввести очередь команд.

### Задачи

1. Добавить сервис `rabbitmq` в `docker-compose.yml`.
2. В `api` реализовать publisher команд в exchange/queue.
3. В `control` реализовать consumer команд с ACK.
4. Определить контракт сообщения команды (JSON schema/version).
5. Настроить durable queue и message persistence.

### Минимальный контракт команды

```json
{
  "schema_version": 1,
  "request_id": "uuid",
  "command": "forward",
  "duration_ms": 1000,
  "created_at": "2026-04-29T10:00:00Z",
  "source": "vision"
}
```

### Критерии готовности

- `api` публикует команду в RabbitMQ.
- `control` считывает команду из очереди и выполняет.
- Сообщение подтверждается ACK только после обработки.

---

## 4. Этап C — статусы выполнения

### Цель

Добавить наблюдаемость исполнения команд.

### Задачи

1. Реализовать канал статусов (`accepted`, `running`, `done`, `failed`).
2. Выбрать транспорт для статусов:
   - отдельная RabbitMQ queue,
   - или callback endpoint в `api`.
3. Сохранять статусы в `api` (in-memory/SQLite/PostgreSQL).
4. Добавить endpoint просмотра статуса по `request_id`.

### Критерии готовности

- По `request_id` можно получить фактический статус команды.
- При ошибке `control` API возвращает диагностируемый `failed` с причиной.

---

## 5. Этап D — hardening и эксплуатация

### Задачи

1. Добавить healthcheck для всех сервисов.
2. Добавить `.env.example` с полным набором env.
3. Ограничить и валидировать команды на входе API.
4. Добавить интеграционные тесты `vision -> api -> queue -> control`.
5. Добавить runbook по recovery (очистка очереди, requeue, dead-letter).

