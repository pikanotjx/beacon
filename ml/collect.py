import cv2
import os
import uuid
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def collect_data(name):
    IMAGES_PATH = f"{BASE_DIR}/faces/" + name

    # Creates a directory for people's images if it doesn't already exist
    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)

    capture = cv2.VideoCapture(0)
    print("Collecting images for {}".format(name))
    time.sleep(2)
    for image_count in range(50):
        print("Collecting image {}".format(image_count))
        _, frame = capture.read()

        image_path = os.path.join(IMAGES_PATH, name+"." +
                                  "{}.jpg".format(str(uuid.uuid1())))

        cv2.imwrite(image_path, frame)
        cv2.imshow("frame", frame)

        time.sleep(1)

        # Waits for the user to press "q" to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


name = input("Who's pictures are being collected? ")
collect_data(name)
