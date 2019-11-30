import cv2
import argparse
import numpy as np

# Аргументы запуска скрипта
# --display [remote, local]
# Выводить ли изображение, если да то куда
# remote - удаленно
# local - локально
parser = argparse.ArgumentParser()
parser.add_argument('-d', "--debug", action="store_true", default=False)
parser.add_argument('-s', "--show", type=str, choices=["remote", "local"], action="store", default=False)
parser.add_argument('none')
args = parser.parse_args()


# Константы
TM_PATH = "templates\\"
CONST_TEMPLATE_SIZE = (10, 15)
TEMPLATE_MATCH_VALUE = 0.85
TEMPLATES = {
    "H": cv2.resize(cv2.imread(f"{TM_PATH}H.png"), CONST_TEMPLATE_SIZE),
    "S": cv2.resize(cv2.imread(f"{TM_PATH}S.png"), CONST_TEMPLATE_SIZE),
    "U": cv2.resize(cv2.imread(f"{TM_PATH}U.png"), CONST_TEMPLATE_SIZE),
}
COLOR_AREA = 100.0
COLORS = {
    "green": [np.array((55, 250, 250), np.uint8), np.array((65, 255, 255), np.uint8)],
    "yellow": [np.array((25, 250, 250), np.uint8), np.array((35, 255, 255), np.uint8)],
    "red": [np.array((0, 250, 250), np.uint8), np.array((10, 255, 255), np.uint8)]
}

if args.debug:
    DEBUG_COLOR = (255, 0, 0)


# Функция поиска контуров в кадре
# Принимает кадр, аргументы трешолда: thresh, maxval
# Возвращает результат выполнения функции cv2.findContours():
def findContours(frame: np.ndarray, _thresh: tuple) -> tuple:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, _thresh[0], _thresh[1], cv2.THRESH_BINARY_INV)
    return cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# Функция поиска самого большого обьекта
# Принимает в себя список полученый из cv2.findContours()
# Возвращает кортеж вида: (x, y, w, h)
# x - координа оX левого верхнего угла
# y - коордтната oY левого верхнего угла
# w - ширина квадрата
# h - высота квадрата
def findBiggestRect(contours_array: list) -> tuple:
    if len(contours_array) > 0:
        sqr, idx = 0, 0
        for index, contour in enumerate(contours_array):
            x, y, w, h = cv2.boundingRect(contour)
            if w * h > sqr:
                sqr = w * h
                idx = index
        return cv2.boundingRect(contours_array[idx])
    else:
        return tuple()


# Функция проверяет есть ли буква в кадре
# Принимает один аргумент: кадр
# Возвращает одну из букв заданых в словаре TEMPLATES
# В случае не удачи возвращает пустую строку
def getLetterFromFrame(frame: np.ndarray) -> str:
    contours, hierarchy = findContours(frame, (55, 255))
    shape = findBiggestRect(contours)

    if len(shape) == 4:
        x, y, w, h = shape
        rect = frame[y:y+h, x:x+w]
        rect = cv2.resize(rect, CONST_TEMPLATE_SIZE)

        for letter in TEMPLATES:
            match = cv2.matchTemplate(rect, TEMPLATES[letter], cv2.TM_CCOEFF_NORMED)
            if match[0][0] >= TEMPLATE_MATCH_VALUE:
                if args.debug:
                    cv2.rectangle(frame, (x-3, y-3), (x+w+3, y+h+3), DEBUG_COLOR, 2)
                return letter

    return ""


# Функция проверяет есть ли цвет в кадре
# Принимает один аргумент: кадр
# Возвращает одну из букв заданых в словаре TEMPLATES
# В случае не удачи возвращает пустую строку
def getColorFromFrame(frame: np.ndarray) -> str:
    hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color in COLORS:
        mask = cv2.inRange(hsvimg, COLORS[color][0], COLORS[color][1])
        moments = cv2.moments(mask, 1)

        if moments['m00'] > COLOR_AREA:

            if args.debug:
                x = int(moments['m10'] / moments['m00'])
                y = int(moments['m01'] / moments['m00'])
                cv2.circle(frame, (x, y), 10, DEBUG_COLOR, -1)

            return color

    return ""


if __name__ == '__main__':
    color_img = cv2.imread("images\\colors\\red.png")
    letter_img = cv2.imread("images\\letters\\__Hus.png")

    print(getLetterFromFrame(letter_img))
    print(getColorFromFrame(color_img))

    if args.show == 'local':
        cv2.imshow("Color", color_img)
        cv2.imshow("Letter", letter_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



