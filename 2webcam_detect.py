import cv2
import numpy as np
import keras
import requests

# Load model
model = keras.saving.load_model("drowsiness.keras")
target_size = (96, 96)

# API URLs
API_CLOSED = "https://iot.roboninja.in/index.php?action=write&UID=NB09&D1=1"
API_OPEN   = "https://iot.roboninja.in/index.php?action=write&UID=NB09&D1=0"

# Counters
closed_count = 0
open_count = 0
THRESHOLD = 15
last_state = None

# FACE detector (works even when eyes are closed)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect face(s)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    label = "NO FACE"

    for (x, y, w, h) in faces:
        # Draw face box
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,0), 2)

        # Crop upper part of the face where eyes always are
        eye_region = gray[y:y + int(h * 0.45), x:x + w]

        # Resize and reshape
        eye_resized = cv2.resize(eye_region, target_size).reshape(1, 96, 96, 1) / 255.0

        # Predict
        pred = model.predict(eye_resized)[0]
        print(f"{pred=}")
        label = "OPEN" if pred[1] > pred[0] else "CLOSED"

        # Count logic
        if label == "CLOSED":
            closed_count += 1
            open_count = 0
        else:
            open_count += 1
            closed_count = 0

        # Trigger IoT API
        if closed_count >= THRESHOLD and last_state != "CLOSED":
            requests.get(API_CLOSED)
            print(">>> SENT: EYES CLOSED")
            last_state = "CLOSED"

        if open_count >= THRESHOLD and last_state != "OPEN":
            requests.get(API_OPEN)
            print(">>> SENT: EYES OPEN")
            last_state = "OPEN"

        break  # Use only one face

    # Show label
    cv2.putText(frame, f"Eyes: {label}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
