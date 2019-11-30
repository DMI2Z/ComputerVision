"""

    Это черновик.
    Все функции после отладки переносятся в другие .py фалы

"""
import cv2
import os
import msvcrt

CAMERAS_DATA = {}
CAMERAS_QUEUE = []


def captureCamera(tag: str = None):
    CAMERAS_DATA.update({tag: [True, '', '']})

    while tag in CAMERAS_DATA:
        if CAMERAS_DATA[tag][0]:
            yield print(tag)
        else:
            yield None


if __name__ == '__main__':
    CAMERAS_QUEUE = [
        captureCamera("First"),
        captureCamera("Second"),
        captureCamera("Third")
    ]

    key = None
    while key != b'27':
        os.system("cls")
        for camera in CAMERAS_QUEUE:
            camera.send(None)

        if msvcrt.kbhit():
            key = msvcrt.getch()

            if key == b'1':
                CAMERAS_DATA["First"][0] = not CAMERAS_DATA["First"][0]

            elif key == b'2':
                CAMERAS_DATA["Second"][0] = not CAMERAS_DATA["Second"][0]

            elif key == b'3':
                CAMERAS_DATA["Third"][0] = not CAMERAS_DATA["Third"][0]
