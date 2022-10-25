import cv2
import numpy as np


def rotate_bound(img, angle=90):
    """
    将img顺时针旋转angle角度
    """
    h, w = img.shape[:2]
    Xcenter, Ycenter = w // 2, h // 2

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    mat = cv2.getRotationMatrix2D((Xcenter, Ycenter), -angle, 1.0)
    cos = np.abs(mat[0, 0])
    sin = np.abs(mat[0, 1])

    # compute the new bounding dimensions of the image
    newW = int((h * sin) + (w * cos))
    newH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    mat[0, 2] += (newW / 2) - Xcenter
    mat[1, 2] += (newH / 2) - Ycenter

    # perform the actual rotation and return the image
    return cv2.warpAffine(img, mat, (newW, newH))


if __name__ == '__main__':
    image = cv2.imread('testShadow.jpg')
    rotateAngle = 90
    imag = rotate_bound(image, rotateAngle)
    cv2.imshow('rotate', imag)
    cv2.waitKey()
