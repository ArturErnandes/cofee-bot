import cv2

from models import Color, ColorMask


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
                    mask=mask,
                )
            )

        return masks
