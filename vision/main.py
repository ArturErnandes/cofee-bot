import cv2

from vision.detectors import ColorsDetector, ObjectsDetector, ObjectsGeometry, Navigator, Visualizer
from vision.config import camera, objects_config, visualizer_config, colors, robot_size
from vision.logger import get_logger


logger = get_logger(__name__)

color_recognizer = ColorsDetector(colors)

object_detector = ObjectsDetector(
    objects_config.kernel,
    objects_config.min_area,
    objects_config.filter_iterations,
)

objects_geometry = ObjectsGeometry()
navigator = Navigator(robot_size)

visualizer = Visualizer(
    visualizer_config.text_color,
    visualizer_config.border_color,
    visualizer_config.thickness)

capture = cv2.VideoCapture(camera)

while True:
    success, frame = capture.read()
    if not success:
        logger.error("Failed to capture frame")
        break

    masks = color_recognizer.create_masks(frame)
    detected_objects = object_detector.detect(masks)
    detected_geometry = objects_geometry.build_geometry(detected_objects)
    navigation_data = navigator.build_navigation(detected_geometry)

    processed_frame = visualizer.visualize(
        frame,
        detected_objects,
        detected_geometry,
        navigation_data,
    )

    cv2.imshow("frames", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
