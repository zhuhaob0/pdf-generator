import cv2
import numpy as np


def correctRect(img, points):
    height, width = img.shape[:2]
    # 同一成一个顺序：左上，左下，右下，右上
    src = np.float32(points)
    # print('src:', src)
    dst = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
    # print('dst:', dst)
    # 获取透视变换矩阵，进行转换
    M = cv2.getPerspectiveTransform(src, dst)
    img = cv2.warpPerspective(img, M, (width, height),
                              borderValue=(255, 255, 255))
    return img
