import cv2
import numpy as np

# image path
img_path = "data\\home.jpg"
blank_mode = False

if blank_mode:
    # reading image (IMAGE_PATH, FLAG: -1 (RGBA) | 0 (GREY) | 1 (RGB))
    img = cv2.imread(img_path, 1)

else:
    # creating a blank image
    img = np.zeros([512, 512, 3], np.uint8)

# drawing a figure from (0, 0) pos to (255, 255), with blue color (BGR)
# line(IMAGE, COORD_FROM, COORD_TO, COLOR, THICKNESS)
img = cv2.line(img, (0, 0), (255, 255), (255, 0, 0), 5)
img = cv2.arrowedLine(img, (0, 300), (255, 300), (255, 0, 0), 5)
img = cv2.rectangle(img, (300, 300), (350, 350), (0, 0, 255), 5)
img = cv2.circle(img, (325, 325), 25, (0, 255, 0), -1)

# drawing a text on the image (IMAGE, TEXT, POSITION, FONT, SIZE, COLOR, THICKNESS)
img = cv2.putText(img, 'OpenCV', (10, 300), 0, 4, (100, 100, 255), 2, cv2.LINE_AA)

# show a window with image and title
cv2.imshow('Home.jpg', img)

# time delay for 1 sec
cv2.waitKey(2000)

# closing all windows
cv2.destroyAllWindows()
