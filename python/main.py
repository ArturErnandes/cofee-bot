import cv2

from detectors import ColorsDetector, ObjectsDetector, Visualizer
from config import camera, objects_config, visualizer_config, colors
from logger import get_logger


logger = get_logger(__name__)

color_recognizer = ColorsDetector(colors)

object_detector = ObjectsDetector(
    objects_config.kernel,
    objects_config.min_area,
    objects_config.filter_iterations,
)

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
    processed_frame = visualizer.visualize(frame, detected_objects)

    cv2.imshow("frames", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
