import cv2


def compute(img):
    img = img.copy()
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img
