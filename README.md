# cofee-bot — gesture-based coffee delivery prototype

Проект демонстрирует прототип системы «жест -> доставка кофе» с двумя реализациями:

- **Python vision/navigation контур**: захват видео, детекция цветовых маркеров, расчёт дистанции/угла до цели и визуализация.
- **C++ control контур**: симуляция исполнительной части робота (движение по командам `forward/right/left/stop`).

Текущий репозиторий — инженерный прототип для лабораторной/исследовательской фазы, а не production-система.

## Состав системы

| Компонент | Реализация | Назначение |
|---|---|---|
| Vision + Navigation | `vision/main.py`, `vision/detectors/` | CV-пайплайн по кадрам камеры и расчёт навигационных параметров |
| API endpoint для команд | `api/app.py` | HTTP-вход для передачи команды (в текущем виде без очереди/диспетчера) |
| Engine control prototype | `control/classes.h`, `control/engine_controll.cpp` | Симуляция реакции движка на текстовые команды |
| Конфигурация CV | `vision/config.py` | HSV-диапазоны, фильтрация масок, параметры визуализации |

## Запуск проекта

Проект поддерживает два режима:

1. Локальный запуск модулей по отдельности (удобно для отладки).
2. Запуск каркаса через Docker Compose (`vision`, `api`, `control`).

---

### Локальный запуск

#### Vision (Python)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m vision.main
```

Остановка окна OpenCV: клавиша `q`.

### FastAPI endpoint

```bash
source .venv/bin/activate
python -m api.run
```

URL: `http://localhost:8080/docs`.

#### Control (C++)

Можно запускать как через CMake, так и через прямую сборку:

```bash
cd control
cmake -S . -B build
cmake --build build
./build/engine_controll
```

Или:

```bash
cd control
g++ -std=c++11 engine_controll.cpp -o engine_controll
./engine_controll
```

---

### Docker Compose (skeleton: 3 контейнера)

```bash
docker compose up --build -d
```

Состав:
- `vision` — CV модуль (OpenCV + камера)
- `api` — FastAPI endpoint
- `control` — C++ control prototype

Проверка статуса:

```bash
docker compose ps
```

Остановка:

```bash
docker compose down
```

Логи:

```bash
docker compose logs -f api
docker compose logs -f vision
docker compose logs -f control
```

Важно:
- текущий compose — каркас без интеграции модулей между собой;
- для `vision` доступны env-overrides:
  - `VISION_CAMERA_INDEX`
  - `VISION_ROBOT_SIZE_CM`
  - `VISION_MIN_AREA`
  - `VISION_FILTER_ITERATIONS`
- на Linux для реальной камеры обычно нужно пробрасывать `device` (`/dev/video*`);
- на macOS/Windows Docker Desktop прямой доступ к хостовой камере обычно ограничен.

## Диаграммы

### Технический комплекс

Показывает физическую и сетевую топологию стенда: камера, сервер, кофемашина и робот, а также их каналы связи на уровне системы.

![Технический комплекс](docs/images/KTS.jpg)

### Use-case диаграмма

Фиксирует функциональные сценарии по участникам системы: какие действия инициирует пользователь и какие сервисные функции выполняют сервер, камера, кофемашина и робот.

![Use-case diagram](docs/images/use-case-schema.png)

### Sequence диаграмма

Отражает основной порядок выполнения операций во времени: от детекции жеста и старта приготовления кофе до доставки, фиксации прибытия и возврата робота на базу.

![Sequence diagram](docs/images/sequence-schema.png)

### Концептуальная модель

Описывает ключевые сущности и их связи на уровне предметной области: поток видео в сервер и управляющие команды от сервера к исполнительным компонентам.

![Concept model](docs/images/concept-model.png)

### UML диаграмма классов

Показывает структуру классов и ответственность модулей прототипа, включая обработку команд, навигационную логику и взаимодействие компонентов.

![UML class diagram](docs/images/uml.png)

## Документация

- [docs/runbook.md](docs/runbook.md) — runbook запуска и диагностики
- [docs/vision-navigation.md](docs/vision-navigation.md) — контракт CV/навигационного пайплайна
- [docs/api.md](docs/api.md) — API-контракт `POST /command`
- [docs/models.md](docs/models.md) — модели данных Python-части
- [docs/engine-control.md](docs/engine-control.md) — C++ контур управления
- [docs/future-tasks.md](docs/future-tasks.md) — план интеграции модулей и RabbitMQ

## Ограничения текущего состояния

- Интеграция между `vision/main.py`, `api/app.py` и C++ контроллером не реализована как единый runtime-контур.
- `POST /command` принимает команду и возвращает подтверждение, но не передаёт её в исполнительный движок.
- Расчёт дистанции зависит от `robot_size` и калибровки сцены; без калибровки значение в см условное.
- В проекте есть базовый список зависимостей в `requirements.txt`, но без зафиксированных версий пакетов.
