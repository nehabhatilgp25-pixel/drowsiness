# Driver Drowsiness Dashboard

This is a dashboard that uses a camera to detect whether a driver's eyes are open or closed and accordingly determines if they are awake or asleep. If they are asleep, a buzzer rings and the online web dashboard displays a screen that informs the user that the driver is asleep.

## Details

First, the "working_eyes.py" file opens the user's webcam on their device (this only works for Apple devices). The program uses CV's eye pre-trained eye detection model to determine if the user's eyes are visible in the frame or not. If the eyes are not visible for longer than 15 frames, the code determines that the driver must have fallen asleep (as this would mean either the driver's eyes are closed or their head must have dropped down). So the program sends an API call to the IoT dashboard at iot.roboninja.in which changes the D1 pin from 0 to 1, hence signalling that the driver is asleep. This causes the WEMOS MINI's buzzer to start buzzing so that the driver can be woken up. Also, the online web dashboard also turns red and displays that the driver has fallen asleep, so any concerned party (like maybe the driver's friends or family) who has the dashboard open can see that the driver is asleep, and accordingly react if they stay asleep for a long time.

## Future Scope

This version of the system is just a prototype. Future versions could include the ESP Cam so that the system can physically be implemented in an actual car (right now it operates on the laptop). Future versions could also check the car's location using GPS and accordingly call the driver's family if the driver is asleep for too long.
