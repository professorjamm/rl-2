import pupil_apriltags as apriltag
from pupil_apriltags import Detector
import cv2
img = cv2.imread('apriltag_foto.jpg', cv2.IMREAD_GRAYSCALE)
detector = apriltag.Detector()
result = detector.detect(img)   
print(result)
