import cv2

from config import camera
from logger import get_logger


logger = get_logger(__name__)

capture = cv2.VideoCapture(camera)

while True:
    success, frame = capture.read()
    if not success:
        logger.error("Failed to capture frame")
        break

    proccessed_frame =

capture.release()
cv2.destroyAllWindows()