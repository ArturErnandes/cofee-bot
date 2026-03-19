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


class ColorRecognizer:
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


'''
class ObjectDetector:
    def __init__(self, min_contour_area=500, kernel_size=(5, 5)):
        self.min_contour_area = min_contour_area
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    def clean_mask(self, mask):
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel, iterations=2)
        return mask

    @staticmethod
    def find_contours(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def detect(self, masks):
        detections = []

        for item in masks:
            cleaned_mask = self.clean_mask(item["mask"])
            contours = self.find_contours(cleaned_mask)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area < self.min_contour_area:
                    continue

                x, y, w, h = cv2.boundingRect(contour)
                detections.append(
                    {
                        "label": item["label"],
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                        "area": area,
                    }
                )

        return detections


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
