# Runbook

Документ описывает практический запуск и проверку `cofee-bot` в текущем состоянии репозитория.

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
pip install opencv-python fastapi uvicorn numpy pydantic
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
