import cv2
import numpy as np
from gui.Interface import createSliderHSV

# web-cam resolution
width = 1280.0
height = 720.0


def callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(param[y, x])


# loading the default camera 0
cam = cv2.VideoCapture(0)

# setting up the camera
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)

color_mask_min = np.array((105, 200, 0), np.uint8)
color_mask_max = np.array((140, 255, 255), np.uint8)

# main loop
if __name__ == '__main__':
    createSliderHSV(color_mask_min, color_mask_max)

    while cam.isOpened():
        ret, frame = cam.read()

        if ret:
            hvs_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hvs_image, color_mask_min, color_mask_max)
            cv2.setMouseCallback("HVS", callback, param=hvs_image)


            moments = cv2.moments(mask, 1)
            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']

            if dArea > 100:
                print("PEN")
                x = int(dM10 / dArea)
                y = int(dM01 / dArea)
                frame = cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

            cv2.imshow("Mask", mask)
            cv2.imshow("Cap", frame)
            cv2.imshow("HVS", hvs_image)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        else:
            break

    cv2.destroyAllWindows()

# releasing web-cam
cam.release()

