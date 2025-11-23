import cv2
import numpy as np
import requests
import time

# API URLs
API_CLOSED = "https://iot.roboninja.in/index.php?action=write&UID=NB09&D1=1"
API_OPEN   = "https://iot.roboninja.in/index.php?action=write&UID=NB09&D1=0"

# Setting counts
closed_count = 0
open_count = 0
THRESHOLD = 15   # number of consecutive frames
last_state = None   # "OPEN" or "CLOSED"

# Eye detector
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml") #loading eye detector.

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION) #opens camera. 0 is default webcam. avfoundation is a specific reader implementation. AVFoundation is for macOS.

while True: #infinite loop
    ret, frame = cap.read() #ret = boolean. TRUE if frame read correctly. frame = frame of video.
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #making the frame grayscaled.

    # Detecting eyes in frame
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    label = "CLOSED" #label set to closed by default.
    detected_eye = None #eyes not detected by default.

    for (x, y, w, h) in eyes: #eyes is the list of rectangles detected.
        detected_eye = gray[y:y+h, x:x+w] #cropping image to extract eye region.
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) #blue rectangle around eye.
        break  # use first detected eye

    if detected_eye is not None: #if eye is open (i.e. eye detected in box).
        # Preprocess
        label = "OPEN" #eye is labelled open.
    else:
        label = "CLOSED" #eye is labelled closed.
    
    # Update counters
    if label == "CLOSED":
        closed_count += 1 #update closed counter by 1
        open_count = 0 #and reset open counter
    else:
        open_count += 1
        closed_count = 0

    # Trigger API for CLOSED
    if closed_count >= THRESHOLD: #only if the threshold is crossed to prevent continuous unnecessary signalling.
        print(">>> Sending CLOSED alert to IoT")
        requests.get(API_CLOSED) #API in iot.roboninja.in
        last_state = "CLOSED"

    # Trigger API for OPEN
    if open_count >= THRESHOLD: #and last_state != "OPEN":
        print(">>> Sending OPEN alert to IoT")
        requests.get(API_OPEN)
        last_state = "OPEN"


    # Display state
    cv2.putText(frame, f"Eyes: {label}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) #Eyes: OPEN/CLOSED text on webcam frame.

    cv2.imshow("Drowsiness Detection", frame) #shows current vid frame.

    if cv2.waitKey(1) & 0xFF == ord('q'): # if q key pressed, program ends.
        break

cap.release() #ends webcam.
cv2.destroyAllWindows() #closes video window.
