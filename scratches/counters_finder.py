import cv2
import numpy as np

if __name__ == '__main__':
    blue = np.array((90, 90, 90), np.uint8)
    blue.put(0, 100)
    print(blue.dtype)
