import cv2
import numpy as np
import msvcrt

# events from cv2
events = [event for event in dir(cv2) if "EVENT" in event]


# mouse click function
def mouse_btn_clicked(event, x, y, flags, param):
    pass


if __name__ == '__main__':
    print(msvcrt.getch())
    input()