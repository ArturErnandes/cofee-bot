import cv2

from models import ColorMask, DetectedObject


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
