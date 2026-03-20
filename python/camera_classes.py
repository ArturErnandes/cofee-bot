from dataclasses import dataclass
import cv2
import numpy as np
from numpy.typing import NDArray


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


class ColorsDetector:
    def __init__(self, colors: list[Color]):
        self.colors = colors

    @staticmethod
    def bgr_to_hsv(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    @staticmethod
    def create_color_mask(hsv_frame, color: Color):
        mask = cv2.inRange(hsv_frame, color.lower_value, color.upper_value)
        return mask

    def create_masks(self, frame):
        masks = []
        hsv_frame = self.bgr_to_hsv(frame)

        for color in self.colors:
            mask = self.create_color_mask(hsv_frame, color)
            masks.append(
                ColorMask(
                    name=color.name,
                    mask=mask
                )
            )

        return masks


class ObjectsDetector:
    def __init__(self, kernel, min_area, filter_iterations):
        self.kernel = kernel
        self.min_area = min_area
        self.filter_iterations = filter_iterations

    def filter_mask(self, color_mask: ColorMask):
        filtered_mask = cv2.erode(color_mask.mask, self.kernel, iterations=self.filter_iterations)
        filtered_mask = cv2.dilate(filtered_mask, self.kernel, iterations=self.filter_iterations)
        return ColorMask(
            name=color_mask.name,
            mask=filtered_mask,
        )

    def detect_objects(self, color_mask: ColorMask):
        detected_objects = []
        contours, _ = cv2.findContours(color_mask.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)

            if area < self.min_area:
                continue

            x_coord, y_coord, width, height = cv2.boundingRect(contour)
            detected_object = DetectedObject(
                name=color_mask.name,
                x_coord=x_coord,
                y_coord=y_coord,
                width=width,
                height=height,
                area=area,
            )
            detected_objects.append(detected_object)
        return detected_objects

    def detect(self, color_masks: list[ColorMask]):
        detected_objects = []

        for color_mask in color_masks:
            filtered_mask = self.filter_mask(color_mask)
            objects = self.detect_objects(filtered_mask)
            detected_objects.extend(objects)

        return detected_objects


class Visualizer:
    def __init__(self, text_color, border_color, thickness):
        self.text_color = text_color
        self.border_color = border_color
        self.thickness = thickness

    def draw(self, frame, detected_object: DetectedObject):
        cv2.rectangle(
            frame,
            (detected_object.x_coord, detected_object.y_coord),
            (
                detected_object.x_coord + detected_object.width,
                detected_object.y_coord + detected_object.height,
            ),
            self.border_color,
            self.thickness,
        )

        cv2.putText(
            frame,
            detected_object.name,
            (detected_object.x_coord, max(detected_object.y_coord - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            self.text_color,
            self.thickness,
        )

    def visualize(self, frame, detected_objects: list[DetectedObject]):
        output = frame.copy()

        for detected_object in detected_objects:
            self.draw(output, detected_object)

        return output