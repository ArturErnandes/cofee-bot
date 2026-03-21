from dataclasses import dataclass
from numpy.typing import NDArray
import numpy as np


@dataclass
class Color:
    name: str
    lower_value: NDArray[np.uint8]
    upper_value: NDArray[np.uint8]


@dataclass
class ColorMask:
    name: str
    mask: NDArray[np.uint8]


@dataclass
class DetectedObject:
    name: str
    x_coord: int
    y_coord: int
    width: int
    height: int
    area: float


@dataclass
class Center:
    x_coord: float
    y_coord: float


@dataclass
class ObjectsConfig:
    kernel: NDArray[np.uint8]
    min_area: int
    filter_iterations: int


@dataclass
class VisualizerConfig:
    text_color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    thickness: int