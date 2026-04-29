# Vision + Navigation Pipeline

Техническая спецификация Python-пайплайна обработки кадра и расчёта навигационных метрик.

- Entry point: `vision/main.py`
- Core implementation: `vision/detectors/`
- Runtime config: `vision/config.py`
- Data contracts: `vision/models.py`

---

## 1. Логическая структура

| Компонент | Вход | Выход | Назначение |
|---|---|---|---|
| `ColorsDetector.create_masks()` | BGR frame (`numpy`) | `list[ColorMask]` | Конвертация BGR->HSV и бинарные маски по цветам |
| `ObjectsDetector.detect()` | `list[ColorMask]` | `list[DetectedObject]` | Морфология + контуры + фильтр по площади |
| `ObjectsGeometry.build_geometry()` | `list[DetectedObject]` | `DetectedGeometry` | Поиск центров и геометрии робота/цели |
| `Navigator.build_navigation()` | `DetectedGeometry` | `NavigationData | None` | Векторы, масштаб px->cm, дистанция и угол |
| `Visualizer.visualize()` | frame + все промежуточные структуры | frame | Отрисовка боксов, векторов, текста |

---

## 2. Контракт конфигурации (`vision/config.py`)

### 2.1 Цветовые диапазоны

Используются 3 логических объекта:

| Имя | Назначение | HSV lower | HSV upper |
|---|---|---|---|
| `front-section` | передняя метка робота | `[145, 120, 120]` | `[175, 255, 255]` |
| `back-section` | задняя метка робота | `[98, 170, 170]` | `[108, 255, 255]` |
| `target` | целевой объект | `[20, 150, 150]` | `[35, 255, 255]` |

### 2.2 Параметры детекции

| Параметр | Значение по умолчанию | Где используется |
|---|---|---|
| `kernel` | `np.ones((5, 5), np.uint8)` | `erode/dilate` |
| `min_area` | `500` | отбрасывание мелких контуров |
| `filter_iterations` | `1` | количество итераций морфологии |
| `robot_size` | `10` | масштабирование px -> см |

`robot_size` трактуется как физическое расстояние между front/back маркерами в сантиметрах.

---

## 3. Алгоритм обработки кадра

Для каждого кадра `capture.read()`:

1. `create_masks(frame)` создаёт маску на каждый `Color`.
2. Для каждой маски выполняется erosion + dilation.
3. По контурам строятся `DetectedObject` (`x, y, width, height, area`).
4. Вычисляются центры `front/back/target`.
5. Если есть `front` и `back`, считается `robot_center`.
6. Если есть все центры (`front/back/robot/target`), считается навигация:
   - `robot_vector = back -> front`
   - `target_vector = robot_center -> target`
   - `scale = robot_size / |robot_vector_px|`
   - `distance_to_target = |target_vector_px| * scale`
   - `target_angle = arccos((robot·target)/(|robot|*|target|))`
7. `Visualizer` отрисовывает геометрию и текст.

---

## 4. Навигационные формулы

### 4.1 Масштаб

`scale_cm_per_px = robot_size_cm / distance(front_center, back_center)_px`

### 4.2 Дистанция до цели

`distance_cm = distance(robot_center, target_center)_px * scale_cm_per_px`

### 4.3 Угол на цель

`angle_deg = degrees(arccos((v_robot · v_target) / (|v_robot| * |v_target|)))`

Ограничение: угол всегда в диапазоне `[0, 180]`, так как используется `arccos` от скалярного произведения без ориентации знака поворота.

---

## 5. Выходные артефакты кадра

`Visualizer` добавляет:

- bounding box + label на каждый `DetectedObject`;
- линия `back -> front` (ориентация робота);
- линия `robot_center -> target` (направление к цели);
- текст:
  - `Distance: X cm`
  - `Angle: Y deg`

Если `NavigationData` отсутствует, показываются только боксы.

---

## 6. Точки отказа и деградация

| Условие | Реакция |
|---|---|
| кадр не получен (`capture.read() == False`) | лог ошибки и остановка цикла |
| объект не найден по цвету | соответствующий центр = `None` |
| неполная геометрия | `Navigator.build_navigation()` возвращает `None` |
| нулевая длина вектора | потенциальное деление на ноль в расчёте угла/масштаба (сейчас без явной защиты) |

---
