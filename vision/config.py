import numpy as np
from vision.models import Color, ObjectsConfig, VisualizerConfig

def fill_colors(colors_dict):
    colors_list = []
    for color in colors_dict:
        colors_list.append(
            Color(
                name=color["name"],
                lower_value=color["lower"],
                upper_value=color["upper"],
            )
        )

    return colors_list


camera = 0

color_ranges = [
    {
        #красный
        "name": "front-section",
        "lower": np.array([145, 120, 120], dtype=np.uint8),
        "upper": np.array([175, 255, 255], dtype=np.uint8),
    },
    {
        #синий
        "name": "back-section",
        "lower": np.array([98, 170, 170], dtype=np.uint8),
        "upper": np.array([108, 255, 255], dtype=np.uint8),
    },
    {
        "name": "target",
        "lower": np.array([20, 150, 150], dtype=np.uint8),
        "upper": np.array([35, 255, 255], dtype=np.uint8),
    }
]

robot_size = 10

kernel = np.ones((5, 5), np.uint8)
min_area = 500
filter_iterations = 1

text_color = (0, 0, 0)
border_color = (0, 0, 0)
thickness = 2

objects_config = ObjectsConfig(
    kernel=kernel,
    min_area=min_area,
    filter_iterations=filter_iterations,
)

visualizer_config = VisualizerConfig(
    text_color=text_color,
    border_color=border_color,
    thickness=thickness,
)

colors = fill_colors(color_ranges)
