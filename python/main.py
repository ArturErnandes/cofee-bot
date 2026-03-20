import cv2

from camera_classes import ColorsDetector, ObjectsDetector, Visualizer
from config import camera, colors, kernel, min_area, filter_iterations, text_color, border_color, thickness
from logger import get_logger


logger = get_logger(__name__)

color_recognizer = ColorsDetector(colors)
object_detector = ObjectsDetector(kernel, min_area, filter_iterations)
visualizer = Visualizer(text_color, border_color, thickness)

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
