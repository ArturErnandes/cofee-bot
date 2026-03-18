import numpy as np


camera = 0

color_ranges = [
    {
        "label": "front-section",
        "lower": np.array([145, 120, 120], dtype=np.uint8),
        "upper": np.array([175, 255, 255], dtype=np.uint8),
    },
    {
        "label": "back-section",
        "lower": np.array([95, 120, 120], dtype=np.uint8),
        "upper": np.array([115, 255, 255], dtype=np.uint8),
    },
]