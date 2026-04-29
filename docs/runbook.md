# Runbook

Документ описывает запуск и проверку `cofee-bot` в двух режимах:
- локально (модули по отдельности),
- через Docker Compose (skeleton из 3 контейнеров).

---

## 1. Предпосылки

| Компонент | Минимум | Назначение |
|---|---|---|
| Python | 3.10+ | запуск CV и API |
| pip | актуальный | установка библиотек |
| Камера | USB / встроенная | источник кадров для `cv2.VideoCapture(camera)` |
| C++ компилятор | `g++`/`clang++` с C++11 | сборка `engine_controll` |

---

## 2. Подготовка Python окружения

Из корня репозитория:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Проверка импортов:

```bash
python -c "import cv2, fastapi, uvicorn, numpy, pydantic; print('ok')"
```

Ожидаемый результат: `ok`.

---

## 3. Запуск CV контура

```bash
source .venv/bin/activate
python -m vision.main
```

Поведение:

1. Открывается окно `frames`.
2. Система выделяет объекты по HSV диапазонам из `vision/config.py`.
3. При обнаружении `front-section`, `back-section`, `target` отрисовываются:
   - bounding boxes;
   - вектор ориентации робота;
   - вектор на цель;
   - `Distance` и `Angle`.

Остановка: клавиша `q`.

---

## 4. Запуск API

```bash
source .venv/bin/activate
python -m api.run
```

Проверка health через OpenAPI UI:
- `http://localhost:8080/docs`

Тест-запрос:

```bash
curl -X POST "http://localhost:8080/command?command=forward&time=1.5"
```

Ожидаемый ответ:

```json
{"message":"Command 'forward' executed successfully"}
```

---

## 5. Запуск C++ control prototype

Сборка через CMake:

```bash
cd control
cmake -S . -B build
cmake --build build
./build/engine_controll
```

Примеры ввода в stdin:

- `stop`
- `forward 1000`
- `right 500`
- `left 700`

Поведение: `FooEngine` печатает действие, ждёт `time_ms`, затем печатает `stop`.

---

## 6. Запуск через Docker Compose (skeleton)

Из корня репозитория:

```bash
docker compose up --build -d
```

Проверка контейнеров:

```bash
docker compose ps
```

Логи:

```bash
docker compose logs -f api
docker compose logs -f vision
docker compose logs -f control
```

Остановка:

```bash
docker compose down
```

### 6.1 Что сейчас делает compose

1. Поднимает три контейнера: `vision`, `api`, `control`.
2. Не реализует передачу команд между модулями (это следующий этап).
3. Готовит конфигурационный каркас для будущей интеграции.

### 6.2 Конфигурация vision через env

`vision/config.py` хранит дефолты, которые можно переопределять:

- `VISION_CAMERA_INDEX`
- `VISION_ROBOT_SIZE_CM`
- `VISION_MIN_AREA`
- `VISION_FILTER_ITERATIONS`

Пример:

```bash
VISION_CAMERA_INDEX=1 VISION_MIN_AREA=700 docker compose up --build -d
```

### 6.3 Камера в контейнере

На Linux для USB/встроенной камеры обычно нужен проброс `device` (`/dev/video0` и т.д.).
На macOS/Windows при Docker Desktop прямой доступ контейнера к камере часто ограничен.

---
