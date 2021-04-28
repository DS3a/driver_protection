import tensorflow.keras as keras
import cv2
import serial
import numpy as np
import time

model = keras.models.load_model("./trained_models/99_test_acc/")

CAM_NO = 0
cap = cv2.VideoCapture(CAM_NO)
serialPort = serial.Serial(port="/dev/ttyACM0", baudrate=9600)


def shock():
    serialPort.write(b'1')
    serialPort.write(b'0')


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
font = cv2.FONT_HERSHEY_SIMPLEX
was_drowsy = False
msg = "safe"
time_init = time.time()
while True:
    ret, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.resize(frame_rgb, (200, 200))
    frame_rgb = frame_rgb.reshape(1, 200, 200, 3)
    prediction = model(frame_rgb)
    pred = np.argmax(prediction)
    classes = ['awake', 'drowsy']
    if classes[pred] == "awake":
        msg = "safe"
        time_init = time.time()
    if classes[pred] == 'drowsy':
        print("drowsy, starting timer")
        deadline = 3-time.time()+time_init
        print("wake up in " + str(deadline) + "seconds")
        if not was_drowsy:
            was_drowsy = True
        if was_drowsy:
            msg = "wake up in " + str(round(deadline, 2)) + "seconds"
            if time.time() - time_init >= 3:
                print("shocking")
                shock()
                msg = "shocking"
                was_drowsy = False

    prob = float(prediction[0][pred])
    prob *= 100
    prob = round(prob, 3)
    print(prob)
    cv2.putText(frame,
    classes[pred]+" Probability = "+str(prob)+"% : "+str(msg),
    (50, 50), font, 0.5,
                (0, 255, 255), 
                2,
                cv2.LINE_4)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
