import numpy as np
from camera_classes import Color


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
        #red
        "name": "front-section",
        "lower": np.array([145, 120, 120], dtype=np.uint8),
        "upper": np.array([175, 255, 255], dtype=np.uint8),
    },
    {
        #blue
        "name": "back-section",
        "lower": np.array([95, 120, 120], dtype=np.uint8),
        "upper": np.array([115, 255, 255], dtype=np.uint8),
    },
]

kernel = np.ones((5, 5), np.uint8)
min_area = 500
filter_iterations = 1

text_color = (0, 0, 0)
border_color = (0, 0, 0)
thickness = 2


colors = fill_colors(color_ranges)