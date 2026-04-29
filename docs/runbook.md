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
cd vision
python main.py
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
cd api
python server.py
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

## 6. Известные проблемы

### 6.1 Пустой кадр / ошибка камеры

Симптом:
- лог `Failed to capture frame`.

Проверки:
1. Убедиться, что камера доступна и не занята другим приложением.
2. Поменять `camera = 0` в `vision/config.py` на другой индекс (`1`, `2`, ...).

### 6.2 Нет навигационных метрик

Симптом:
- боксы видны частично, `Distance/Angle` отсутствуют.

Причина:
- для расчёта нужны все 3 объекта: `front-section`, `back-section`, `target`.

Действия:
1. Скорректировать HSV диапазоны в `vision/config.py` под освещение.
2. Проверить `min_area`/`filter_iterations`.

---

## 7. Что проверять перед демо

1. Камера стабильно отдаёт кадры > 2 минут.
2. Все три маркера устойчиво детектируются при целевом освещении.
3. `Distance` и `Angle` обновляются без резких скачков на статичной сцене.
4. API `POST /command` отвечает `200` на валидные параметры.
5. C++ бинарь принимает команды `forward/right/left/stop`.
