import cv2
import numpy as np
import keras

# Load model
model = keras.saving.load_model("drowsiness.h5")

# Webcam index 0 means your laptop's default camera
cap = cv2.VideoCapture(0)

target_size = (96, 96)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize to model size
    resized = cv2.resize(gray, target_size)

    # Normalize and reshape
    img = resized.reshape(1, 96, 96, 1) / 255.0

    # Predict
    pred = model.predict(img)[0]

    label = "OPEN" if pred[1] > pred[0] else "CLOSED"

    # Display on screen
    cv2.putText(frame, f"Eyes: {label}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Drowsiness Detection", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
