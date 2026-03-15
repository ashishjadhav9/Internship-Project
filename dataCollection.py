import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

# === SETTINGS ===
offset = 20
imgSize = 300
folder = "Data/SPACE"
counter = 0

# === IP WEBCAM URL (Change IP to your phone's) ===
ip_webcam_url = "http://10.110.83.37:8080/video"  # Replace with your IP Webcam link

cap = cv2.VideoCapture(ip_webcam_url)
detector = HandDetector(maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        print("⚠️ Cannot access IP Webcam feed")
        break

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        if imgCrop.size != 0:  # Avoid errors when crop is empty
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(f"✅ Saved Image {counter}")

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
