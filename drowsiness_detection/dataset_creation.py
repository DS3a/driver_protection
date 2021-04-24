import cv2
import matplotlib.pyplot as plt
import numpy as np
import time


DATASET_FOLDER = "./datasets"
IMGS_FOLDER = "./datasets/imgs"
TIME_TO_CAPTURE = 20 # Seconds
CAM_NO = 2

cap = cv2.VideoCapture(CAM_NO)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
def capture_imgs(time_to_cap, folder, save_as, ind=1):
    time_init = time.time()
    while time.time() - time_init <= time_to_cap:
        ret, frame = cap.read()
        filename = str(ind) + ".jpg"
        ind += 1
        cv2.imshow('frame', frame)
        cv2.imwrite(str(folder)+'/'+str(save_as)+'/'+filename, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_imgs(TIME_TO_CAPTURE, IMGS_FOLDER, "awake", 1717)