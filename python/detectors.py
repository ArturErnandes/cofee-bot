import cv2
import numpy as np

from classes import Color, ColorMask, DetectedObject, Center, Vector, DetectedGeometry, NavigationData


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


class ObjectsGeometry:
    @staticmethod
    def find_object_center(detected_object: DetectedObject):
        return Center(
            x_coord=detected_object.x_coord + detected_object.width / 2,
            y_coord=detected_object.y_coord + detected_object.height / 2,
        )

    @staticmethod
    def find_object_by_name(objects: list[DetectedObject], name: str):
        for detected_object in objects:
            if detected_object.name == name:
                return detected_object
        return None

    @staticmethod
    def find_robot_center(front_center: Center, back_center: Center):
        return Center(
            x_coord=(front_center.x_coord + back_center.x_coord) / 2,
            y_coord=(front_center.y_coord + back_center.y_coord) / 2,
        )

    def build_geometry(self, detected_objects: list[DetectedObject]):
        front_object = self.find_object_by_name(detected_objects, "front-section")
        back_object = self.find_object_by_name(detected_objects, "back-section")
        target_object = self.find_object_by_name(detected_objects, "target")

        front_center = self.find_object_center(front_object) if front_object else None
        back_center = self.find_object_center(back_object) if back_object else None
        target_center = self.find_object_center(target_object) if target_object else None

        robot_center = None
        if front_center and back_center:
            robot_center = self.find_robot_center(front_center, back_center)

        return DetectedGeometry(
            front_center=front_center,
            back_center=back_center,
            target_center=target_center,
            robot_center=robot_center,
        )


class Navigator:
    def __init__(self, robot_size: float):
        self.robot_size = robot_size

    @staticmethod
    def get_vector(start: Center, end: Center):
        return Vector(
            x=end.x_coord - start.x_coord,
            y=end.y_coord - start.y_coord,
        )

    @staticmethod
    def get_vector_length(vector: Vector):
        return (vector.x ** 2 + vector.y ** 2) ** 0.5

    def get_scale(self, front_center: Center, back_center: Center):
        robot_vector = self.get_vector(back_center, front_center)
        pixel_distance = self.get_vector_length(robot_vector)

        return self.robot_size / pixel_distance

    def get_distance_to_target(self, robot_center: Center, target_center: Center, scale: float):
        target_vector = self.get_vector(robot_center, target_center)
        pixel_distance = self.get_vector_length(target_vector)

        return pixel_distance * scale

    @staticmethod
    def get_target_angle(robot: Vector, target: Vector):
        scalar_product = (robot.x * target.x + robot.y * target.y)

        robot_length = Navigator.get_vector_length(robot)
        target_length = Navigator.get_vector_length(target)

        cos_angle = scalar_product / (robot_length * target_length)
        angle = np.arccos(cos_angle)

        return np.degrees(angle)

    def build_navigation(self, data: DetectedGeometry):
        if not all([data.front_center, data.back_center, data.robot_center, data.target_center]):
            return None

        robot_vector = self.get_vector(data.back_center, data.front_center)
        target_vector = self.get_vector(data.robot_center, data.target_center)

        scale = self.get_scale(data.front_center, data.back_center)
        distance_to_target = self.get_distance_to_target(data.robot_center, data.target_center, scale)
        target_angle = self.get_target_angle(robot_vector, target_vector)

        return NavigationData(
            robot_vector=robot_vector,
            target_vector=target_vector,
            distance_to_target=distance_to_target,
            target_angle=target_angle,
        )


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