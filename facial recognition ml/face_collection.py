import cv2
import os
import uuid
import time

def collect_data(name):
    IMAGES_PATH = "C:/Users/Tristan Sim/OneDrive/Documents/GitHub/sutdwasdoftime/facial recognition ml/image_data/" + name

    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)

    cap = cv2.VideoCapture(0)

    print('Collecting images for {}'.format(name))
    time.sleep(2)
    for imgnum in range(50):   
        print('Collecting image {}'.format(imgnum))
        ret, frame = cap.read()

        imgname = os.path.join(IMAGES_PATH,name+'.'+'{}.jpg'.format(str(uuid.uuid1())))

        cv2.imwrite(imgname, frame)
        cv2.imshow('frame', frame)

        time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


collect_data("Jasmine")