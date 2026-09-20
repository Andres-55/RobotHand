import cv2
import mediapipe as mp
import serial
import time
import math
from numpy import interp

# Arduino Serial Port Setup
arduino = serial.Serial('COM3', 9600)  # Change COM3 to your correct port
time.sleep(2)  # Give Arduino time to reset

# MediaPipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Distance Function
def get_distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

# Camera Setup
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]

        # Thumb
        thumbB = handLms.landmark[0]
        thumbT = handLms.landmark[4]
        tReference = handLms.landmark[2]
        trDistance = get_distance(tReference, thumbB)
        tDistance = get_distance(thumbT, thumbB)
        tDistance /= trDistance

        # Index
        indexB = handLms.landmark[0]
        indexT = handLms.landmark[8]
        iReference = handLms.landmark[5]
        irDistance = get_distance(iReference, indexB)
        iDistance = get_distance(indexT, indexB)
        iDistance /= irDistance

        # Middle
        middleB = handLms.landmark[0]
        middleT = handLms.landmark[12]
        mReference = handLms.landmark[9]
        mrDistance = get_distance(mReference, middleB)
        mDistance = get_distance(middleT, middleB)
        mDistance /= mrDistance

        # Ring
        ringB = handLms.landmark[0]
        ringT = handLms.landmark[16]
        rReference = handLms.landmark[13]
        rrDistance = get_distance(rReference, ringB)
        rDistance = get_distance(ringT, ringB)
        rDistance /= rrDistance

        # Pinky
        pinkyB = handLms.landmark[0]
        pinkyT = handLms.landmark[20]
        pReference = handLms.landmark[17]
        prDistance = get_distance(pReference, pinkyB)
        pDistance = get_distance(pinkyT, pinkyB)
        pDistance /= prDistance


        # Map distance (adjust if needed)
        # Example: 0.50 (bent) to 1.00 (straight)
        tAngle = int(interp(tDistance, [1.21, 1.73], [180, 0]))
        tAngle = max(0, min(180, tAngle))  # Clamp to safe servo range

        iAngle = int(interp(iDistance, [0.81, 1.78], [180, 0]))
        iAngle = max(0, min(180, iAngle))  # Clamp to safe servo range

        mAngle = int(interp(mDistance, [0.73, 1.87], [180, 0]))
        mAngle = max(0, min(180, mAngle))  # Clamp to safe servo range

        rAngle = int(interp(rDistance, [0.69, 1.90], [180, 0]))
        rAngle = max(0, min(180, rAngle))  # Clamp to safe servo range

        pAngle = int(interp(pDistance, [0.73, 1.75], [180, 0]))
        pAngle = max(0, min(180, pAngle))  # Clamp to safe servo range

        print(f"Distance: {tDistance:.4f}, Angle: {tAngle}  "
              f"Distance: {iDistance:.4f}, Angle: {iAngle}  "
              f"Distance: {mDistance:.4f}, Angle: {mAngle}  "
              f"Distance: {rDistance:.4f}, Angle: {rAngle}  "
              f"Distance: {pDistance:.4f}, Angle: {pAngle}  ")
        try:
            arduino.write(f"{tAngle},{iAngle},{mAngle},{rAngle},{pAngle}\n".encode())
        except:
            print("Serial connection error.")

        mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    else:
        # No hand detected: send a safe default
        arduino.write(b"0,0,0,0,0\n")

    cv2.imshow("Index Finger Tracker", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
