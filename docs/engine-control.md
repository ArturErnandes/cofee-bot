# Engine Control (C++)

Техническая спецификация C++ контура управления исполнительной частью.

- Entry point: `control/engine_controll.cpp`
- Реализация интерфейсов: `control/classes.h`

---

## 1. Логическая структура

| Компонент | Роль | Ключевые методы |
|---|---|---|
| `AEngine` | Абстракция исполнительного движка | `forward`, `right`, `left`, `stop` |
| `FooEngine` | Демо-реализация движка | печать действия + `sleep_for` + `stop` |
| `ACmdReceiver` | Абстракция источника команд | `receive()` |
| `FooCmdReceiver` | Демо-приём команд из stdin | чтение `string` через `cin` |
| `ControlSystem` | Координатор receiver + engine | `run()` |

---

## 2. Контракт команд

Поддерживаемые команды:

| Команда | Доп. параметр | Поведение |
|---|---|---|
| `stop` | нет | немедленный вызов `engine->stop()` |
| `forward` | `time_ms` (`int`) | движение вперёд, затем `stop` |
| `right` | `time_ms` (`int`) | поворот/движение вправо, затем `stop` |
| `left` | `time_ms` (`int`) | поворот/движение влево, затем `stop` |

Формат stdin:

- `stop`
- `forward 1000`
- `right 500`
- `left 700`

---

## 3. Алгоритм `ControlSystem.run()`

1. Получает `cmd = receiver->receive()`.
2. Если `cmd == "stop"`, вызывает `engine->stop()`.
3. Иначе читает `time_ms` из `cin`.
4. Ветвление:
   - `forward` -> `engine->forward(time_ms)`
   - `right` -> `engine->right(time_ms)`
   - `left` -> `engine->left(time_ms)`

Сценарий одношаговый: `run()` обрабатывает одну команду и завершает выполнение процесса.

---

## 4. Сборка и запуск

### 4.1 Текущий рабочий путь

```bash
cd control
cmake -S . -B build
cmake --build build
./build/engine_controll
```

### 4.2 Альтернативная сборка

```bash
cd control
g++ -std=c++11 engine_controll.cpp -o engine_controll
./engine_controll
```

---

## 5. Ограничения и риски

1. Нет цикла постоянной обработки команд (`while`), только single-shot обработка.
2. Нет обработки неизвестных команд и ошибок ввода.
3. Нет связи с HTTP API `api/server.py`.
4. `FooEngine` — симуляция через `stdout`, без реального драйвера моторов.

---

## 6. Целевое направление развития

1. Выделить протокол обмена командами между Python и C++ (HTTP/gRPC/queue/socket).
2. Добавить очередь и ack-статус выполнения команд.
3. Добавить интеграционные тесты `command -> engine action`.
