import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector()

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lm_list, bbox = detector.findPosition(img, draw=False)
    if len(lm_list) > 0:
        print(lm_list[0])  # See exactly what format it returns
        break

cap.release()