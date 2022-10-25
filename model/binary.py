import cv2


def compute(img):
    img = img.copy()
    _, thresh = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    img = cv2.imread('1.jpg', 0)
    img = compute(img)
    plt.imshow(img)
    plt.show()
