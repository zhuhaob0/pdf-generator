import cv2
import numpy as np


def compute(img):
    img = img.copy()
    kernel_size = img.shape[0] // 50
    if kernel_size % 2 == 0:
        kernel_size += 1
    blur = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    blur[blur < 255] += 1
    img[img < 255] += 1
    result = img / blur * 255
    result[result > 255] = 255
    return result.astype(np.uint8)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import binary
    img = cv2.imread('5.jpg', 0)
    img = binary.compute(img)
    img = compute(img)
    plt.imshow(img, cmap='gray')
    plt.show()
