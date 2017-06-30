import numpy as np
import cv2
import sounddevice as sd


def make_array_to_sound(array, band=0):

    sound = array[:, :, band]
    s = sound.reshape(sound.shape[0] * sound.shape[1])
    sd.play(s, blocking=True)


cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #make_array_to_sound(frame, band=1)
    # Display the resulting frame
    #cv2.imshow('frame',gray)
    cv2.imshow("frame-by-frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
