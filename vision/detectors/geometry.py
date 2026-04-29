from models import Center, DetectedGeometry, DetectedObject


class ObjectsGeometry:
    def __init__(self):
        pass

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
