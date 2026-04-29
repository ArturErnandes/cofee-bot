import numpy as np

from models import Center, DetectedGeometry, NavigationData, Vector


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
