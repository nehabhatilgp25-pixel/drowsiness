import cv2
import numpy as np
import keras
import requests
import time

# Load model
#model = keras.saving.load_model("drowsiness.keras")
target_size = (96, 96)

# API URLs
API_CLOSED = "https://iot.roboninja.in/index.php?action=write&UID=NB09&D1=1"
API_OPEN   = "https://iot.roboninja.in/index.php?action=write&UID=NB09&D1=0"

# States
closed_count = 0
open_count = 0
THRESHOLD = 15   # number of consecutive frames

last_state = None   # "OPEN" or "CLOSED"

# Eye detector
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in frame
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    label = "CLOSED"
    detected_eye = None

    for (x, y, w, h) in eyes:
        detected_eye = gray[y:y+h, x:x+w]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        break  # use first detected eye

    if detected_eye is not None:
        # Preprocess
        label = "OPEN"
    else:
        label = "CLOSED"
    
    # Update counters
    if label == "CLOSED":
        closed_count += 1
        open_count = 0
    else:
        open_count += 1
        closed_count = 0

    # Trigger API for CLOSED
    if closed_count >= THRESHOLD: # and last_state != "CLOSED":
        print(">>> Sending CLOSED alert to IoT")
        requests.get(API_CLOSED)
        last_state = "CLOSED"

    # Trigger API for OPEN
    if open_count >= THRESHOLD: #and last_state != "OPEN":
        print(">>> Sending OPEN alert to IoT")
        requests.get(API_OPEN)
        last_state = "OPEN"


    # Display state
    cv2.putText(frame, f"Eyes: {label}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
