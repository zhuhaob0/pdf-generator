import cv2

def compute(img):
    blur = cv2.GaussianBlur(img, (0, 0), 5)
    usm = cv2.addWeighted(img, 1.5, blur, -0.5, 0)
    return usm


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    img = cv2.imread('1.png')
    img = compute(img)
    plt.imshow(img, cmap='gray')
    plt.show()
