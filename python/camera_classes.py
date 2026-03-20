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
    def create_color_mask(hsv_frame, color):
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
        filtered_mask = cv2.erode(color_mask.mask, self.kernel, self.filter_iterations)
        filtered_mask = cv2.dilate(filtered_mask, self.kernel, self.filter_iterations)
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

    def proceed_objects(self, color_masks: list[ColorMask]):
        detected_objects = []

        for color_mask in color_masks:
            filtered_mask = self.filter_mask(color_mask)
            objects = self.detect_objects(filtered_mask)
            detected_objects.extend(objects)
        return detected_objects



'''
class Visualizer:
    def __init__(self, rectangle_color=(0, 0, 0), text_color=(0, 0, 0), thickness=2):
        self.rectangle_color = rectangle_color
        self.text_color = text_color
        self.thickness = thickness

    def draw(self, frame, detections):
        output = frame.copy()

        for detection in detections:
            x = detection["x"]
            y = detection["y"]
            w = detection["w"]
            h = detection["h"]

            cv2.rectangle(
                output,
                (x, y),
                (x + w, y + h),
                self.rectangle_color,
                self.thickness,
            )
            cv2.putText(
                output,
                detection["label"],
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                self.text_color,
                self.thickness,
            )

        return output'''