import cv2

from camera_classes import ColorRecognizer, ObjectDetector, Visualizer
from config import camera, colors
from logger import get_logger


logger = get_logger(__name__)

color_recognizer = ColorRecognizer(colors)
object_detector = ObjectDetector()
visualizer = Visualizer()

capture = cv2.VideoCapture(camera)

while True:
    success, frame = capture.read()
    if not success:
        logger.error("Failed to capture frame")
        break

    masks = color_recognizer.create_masks(frame)
    detections = object_detector.detect(masks)
    processed_frame = visualizer.draw(frame, detections)

    cv2.imshow("frames", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
