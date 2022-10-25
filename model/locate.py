import cv2
import numpy as np


def locate(img):
    # 预处理
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    height, width = img.shape[:2]
    dst_width = 600  # 目标图像宽度
    scale_ratio = dst_width / width  # 缩放比例
    img_reshape = cv2.resize(
        img, (dst_width, int(height * scale_ratio)))  # 缩放图像
    img_blur = cv2.GaussianBlur(img_reshape, (3, 3), 0)  # 高斯模糊
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_blur, kernel)  # 膨胀
    img_edges = cv2.Canny(img_dilate, 20, 150)  # 提取边缘

    # 寻找轮廓
    contours, _ = cv2.findContours(
        img_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    max_cont = max(contours, key=lambda c: c.shape[0])
    img_cont = np.zeros(img_reshape.shape, dtype=np.uint8)
    cv2.drawContours(img_cont, max_cont, -1, 255, 1)

    # 霍夫变换
    hough_lines = cv2.HoughLines(img_cont, 1, np.pi / 180, 100)

    lines = []
    for line in hough_lines:
        rho = line[0][0]  # 第一个元素是距离rho
        theta = line[0][1]  # 第二个元素是角度theta
        if (theta < (np.pi/4)) or (theta > (3.*np.pi/4)):  # 垂直直线
            pt1 = (int(rho/np.cos(theta)), 0)  # 该直线与第一行的交点
            # 该直线与最后一行的焦点
            pt2 = (
                int((rho-img_reshape.shape[0]*np.sin(theta))/np.cos(theta)), img_reshape.shape[0])
        else:  # 水平直线
            pt1 = (0, int(rho/np.sin(theta)))               # 该直线与第一列的交点
            # 该直线与最后一列的交点
            pt2 = (img_reshape.shape[1], int(
                (rho-img_reshape.shape[1]*np.cos(theta))/np.sin(theta)))
        lines.append(
            (pt1, pt2, (int((pt1[0]+pt2[0])/2), int((pt1[1]+pt2[1])/2))))

    # 选择所围面积最大的四条线
    l1 = [l for l in lines if l[2][0] == img_reshape.shape[1] // 2]
    l2 = [l for l in lines if l[2][1] == img_reshape.shape[0] // 2]
    l1.sort(key=lambda l: l[2][1])
    l2.sort(key=lambda l: l[2][0])
    lines = [l1[0], l2[0], l1[-1], l2[-1]]

    # 计算顶点坐标
    points = []
    for i, j in [[0, 1], [0, 3], [2, 3], [1, 2]]:
        x1, y1 = lines[i][0]
        x2, y2 = lines[i][1]
        x3, y3 = lines[j][0]
        x4, y4 = lines[j][1]
        x = ((x3 - x4) * (x2 * y1 - x1 * y2) - (x1 - x2) * (x4 * y3 - x3 * y4)
             ) / ((x3 - x4) * (y1 - y2) - (x1 - x2) * (y3 - y4))
        y = ((y3 - y4) * (y2 * x1 - y1 * x2) - (y1 - y2) * (y4 * x3 - y3 * x4)
             ) / ((y3 - y4) * (x1 - x2) - (y1 - y2) * (x3 - x4))
        points.append((x, y))

    # 排序角点
    points.sort(key=lambda x: x[0])
    p1 = sorted(points[:2], key=lambda x: x[1])
    p2 = sorted(points[2:], key=lambda x: x[1], reverse=True)
    points = p1 + p2
    points = np.array(points)

    # 计算缩放前坐标
    points /= scale_ratio
    points = points.astype(np.int_)
    points[points[:, 0] >= width, 0] = width
    points[points[:, 0] < 0, 0] = 0
    points[points[:, 1] >= height, 1] = height
    points[points[:, 1] < 0, 1] = 0

    return points
