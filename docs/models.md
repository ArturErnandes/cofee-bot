# Python Data Models

Техническая спецификация структур данных Python-модуля.

- Источник: `python/classes.py`

---

## 1. Список моделей

| Модель | Тип | Назначение |
|---|---|---|
| `Color` | `dataclass` | HSV-диапазон логического цвета |
| `ColorMask` | `dataclass` | Бинарная маска по цвету |
| `DetectedObject` | `dataclass` | Объект, найденный по контуру |
| `Center` | `dataclass` | Центр объекта в пикселях |
| `Vector` | `dataclass` | Вектор в 2D |
| `DetectedGeometry` | `dataclass` | Набор центров робота и цели |
| `NavigationData` | `dataclass` | Расчётные навигационные метрики |
| `ObjectsConfig` | `dataclass` | Параметры фильтрации контуров |
| `VisualizerConfig` | `dataclass` | Параметры отрисовки |
| `Command` | `pydantic.BaseModel` | Вход API-команды |

---

## 2. Поля моделей

### 2.1 `Color`

| Поле | Тип | Описание |
|---|---|---|
| `name` | `str` | Логическое имя (`front-section`, `back-section`, `target`) |
| `lower_value` | `NDArray[np.uint8]` | Нижняя граница HSV |
| `upper_value` | `NDArray[np.uint8]` | Верхняя граница HSV |

### 2.2 `ColorMask`

| Поле | Тип | Описание |
|---|---|---|
| `name` | `str` | Имя цвета |
| `mask` | `NDArray[np.uint8]` | Бинарная маска изображения |

### 2.3 `DetectedObject`

| Поле | Тип | Описание |
|---|---|---|
| `name` | `str` | Тип объекта (совпадает с цветом) |
| `x_coord` | `int` | X левого верхнего угла bbox |
| `y_coord` | `int` | Y левого верхнего угла bbox |
| `width` | `int` | Ширина bbox |
| `height` | `int` | Высота bbox |
| `area` | `float` | Площадь контура |

### 2.4 `Center`

| Поле | Тип | Описание |
|---|---|---|
| `x_coord` | `float` | X-координата центра |
| `y_coord` | `float` | Y-координата центра |

### 2.5 `Vector`

| Поле | Тип | Описание |
|---|---|---|
| `x` | `float` | Проекция по X |
| `y` | `float` | Проекция по Y |

### 2.6 `DetectedGeometry`

| Поле | Тип | Описание |
|---|---|---|
| `front_center` | `Center | None` | Центр передней метки |
| `back_center` | `Center | None` | Центр задней метки |
| `robot_center` | `Center | None` | Центр робота (midpoint front/back) |
| `target_center` | `Center | None` | Центр цели |

### 2.7 `NavigationData`

| Поле | Тип | Описание |
|---|---|---|
| `robot_vector` | `Vector` | Вектор ориентации `back -> front` |
| `target_vector` | `Vector` | Вектор `robot_center -> target` |
| `distance_to_target` | `float` | Расстояние до цели в см |
| `target_angle` | `float` | Угол между `robot_vector` и `target_vector` |

### 2.8 `ObjectsConfig`

| Поле | Тип | Описание |
|---|---|---|
| `kernel` | `NDArray[np.uint8]` | Ядро морфологии |
| `min_area` | `int` | Порог площади контура |
| `filter_iterations` | `int` | Число итераций `erode/dilate` |

### 2.9 `VisualizerConfig`

| Поле | Тип | Описание |
|---|---|---|
| `text_color` | `tuple[int, int, int]` | Цвет текста (BGR) |
| `border_color` | `tuple[int, int, int]` | Цвет рамок/линий (BGR) |
| `thickness` | `int` | Толщина линий и шрифта |

### 2.10 `Command`

| Поле | Тип | Описание |
|---|---|---|
| `message` | `str` | Команда движения |
| `time` | `float` | Время/длительность команды |

---

## 3. Поток данных между моделями

1. `Color` -> `ColorMask`
2. `ColorMask` -> `DetectedObject`
3. `DetectedObject` -> `DetectedGeometry`
4. `DetectedGeometry` -> `NavigationData`
5. `Command` создаётся отдельно в API-слое

---

## 4. Ограничения типовой модели

1. В `NavigationData` нет признака валидности; в pipeline используется `None` как сигнал отсутствия расчёта.
2. Единицы измерения `distance_to_target` зависят от `robot_size` и калибровки.
3. `Command.time` не фиксирует единицы измерения (секунды/миллисекунды) на уровне контракта.
