import tensorflow.keras as keras
import cv2
import numpy as np

model = keras.models.load_model("./trained_models/99_test_acc/")

CAM_NO = 2
cap = cv2.VideoCapture(CAM_NO)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.resize(frame_rgb, (200, 200))
    frame_rgb = frame_rgb.reshape(1, 200, 200, 3)
    prediction = model(frame_rgb)
    pred = np.argmax(prediction)
    classes = ['awake', 'drowsy']
    prob = float(prediction[0][pred])
    prob *= 100
    prob = round(prob, 3)
    print(prob)
    cv2.putText(frame, 
    classes[pred]+" Probability = "+str(prob)+"%", 
    (50, 50), font, 1, 
                (0, 255, 255), 
                2, 
                cv2.LINE_4)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_imgs(TIME_TO_CAPTURE, IMGS_FOLDER, "awake", 1717)