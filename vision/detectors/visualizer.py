import cv2

from models import Center, DetectedGeometry, DetectedObject, NavigationData


class Visualizer:
    def __init__(self, text_color, border_color, thickness):
        self.text_color = text_color
        self.border_color = border_color
        self.thickness = thickness

    def draw(self, frame, detected_object: DetectedObject):
        cv2.rectangle(
            frame,
            (detected_object.x_coord, detected_object.y_coord),
            (detected_object.x_coord + detected_object.width, detected_object.y_coord + detected_object.height),
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

    def draw_vector(self, frame, start: Center, end: Center):
        cv2.line(
            frame,
            (int(start.x_coord), int(start.y_coord)),
            (int(end.x_coord), int(end.y_coord)),
            self.border_color,
            self.thickness,
        )

    def draw_navigation(self, frame, detected_geometry: DetectedGeometry, navigation_data: NavigationData):
        self.draw_vector(frame, detected_geometry.back_center, detected_geometry.front_center)
        self.draw_vector(frame, detected_geometry.robot_center, detected_geometry.target_center)

        text_x = int((detected_geometry.robot_center.x_coord + detected_geometry.target_center.x_coord) / 2)
        text_y = int((detected_geometry.robot_center.y_coord + detected_geometry.target_center.y_coord) / 2)

        distance_text = f"Distance: {navigation_data.distance_to_target:.1f} cm"
        angle_text = f"Angle: {navigation_data.target_angle:.1f} deg"

        cv2.putText(
            frame,
            distance_text,
            (text_x, text_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            self.text_color,
            self.thickness,
        )

        cv2.putText(
            frame,
            angle_text,
            (text_x, text_y + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            self.text_color,
            self.thickness,
        )

    def visualize(self, frame, detected_objects, detected_geometry: DetectedGeometry | None, navigation_data: NavigationData | None):
        output = frame.copy()

        for detected_object in detected_objects:
            self.draw(output, detected_object)

        if detected_geometry and navigation_data:
            self.draw_navigation(output, detected_geometry, navigation_data)

        return output
