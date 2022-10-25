import cv2


def remove(img):
    # 1. 定义腐蚀和膨胀的结构化元素和迭代次数
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    iterNum = 15
    # 2. 将灰度图进行闭运算操作
    imgClose = cv2.morphologyEx(
        img, cv2.MORPH_CLOSE, kernal, anchor=(-1, -1), iterations=iterNum)
    # cv2.imshow('close', imgClose)
    # 3. 闭运算后的图减去原灰度图再进行取反操作
    dst = cv2.bitwise_not(imgClose - img)
    # 4. 使用规一化将原来背景白色的改了和原来灰度图差不多的灰色
    dst = cv2.normalize(dst, None, alpha=0, beta=200,
                        norm_type=cv2.NORM_MINMAX)
    return dst


# def max_filtering(N, I_temp):
#     wall = np.full((I_temp.shape[0]+(N//2)*2, I_temp.shape[1]+(N//2)*2), -1)
#     wall[(N//2):wall.shape[0]-(N//2), (N//2):wall.shape[1]-(N//2)] = I_temp.copy()
#     temp = np.full((I_temp.shape[0]+(N//2)*2, I_temp.shape[1]+(N//2)*2), -1)
#     for y in range(0,wall.shape[0]):
#         for x in range(0,wall.shape[1]):
#             if wall[y,x]!=-1:
#                 window = wall[y-(N//2):y+(N//2)+1,x-(N//2):x+(N//2)+1]
#                 num = np.amax(window)
#                 temp[y,x] = num
#     A = temp[(N//2):wall.shape[0]-(N//2), (N//2):wall.shape[1]-(N//2)].copy()
#     return A
#
#
# def min_filtering(N, A):
#     wall_min = np.full((A.shape[0]+(N//2)*2, A.shape[1]+(N//2)*2), 300)
#     wall_min[(N//2):wall_min.shape[0]-(N//2), (N//2):wall_min.shape[1]-(N//2)] = A.copy()
#     temp_min = np.full((A.shape[0]+(N//2)*2, A.shape[1]+(N//2)*2), 300)
#     for y in range(0,wall_min.shape[0]):
#         for x in range(0,wall_min.shape[1]):
#             if wall_min[y,x]!=300:
#                 window_min = wall_min[y-(N//2):y+(N//2)+1,x-(N//2):x+(N//2)+1]
#                 num_min = np.amin(window_min)
#                 temp_min[y,x] = num_min
#     B = temp_min[(N//2):wall_min.shape[0]-(N//2), (N//2):wall_min.shape[1]-(N//2)].copy()
#     return B
#
#
# def background_subtraction(I, B):
#     O = I - B
#     norm_img = cv2.normalize(O, None, 0,255, norm_type=cv2.NORM_MINMAX)
#     return norm_img
#
#
# def min_max_filtering(M, N, I):
#     if M == 0:
#         #max_filtering
#         A = max_filtering(N, I)
#         #min_filtering
#         B = min_filtering(N, A)
#         #subtraction
#         normalised_img = background_subtraction(I, B)
#     elif M == 1:
#         #min_filtering
#         A = min_filtering(N, I)
#         #max_filtering
#         B = max_filtering(N, A)
#         #subtraction
#         normalised_img = background_subtraction(I, B)
#     return normalised_img
#
#
# if __name__ == '__main__':
#     P = cv2.imread('test3.png', 0)
#     plt.imshow(P, cmap='gray')
#     plt.title("original image")
#     plt.show()
#     # We can edit the N and M values here for P and C images
#     O_P = min_max_filtering(M=1, N=20, I=P)
#
#     # Display final output
#     plt.imshow(O_P, cmap='gray')
#     plt.title("Final output")
#     plt.show()
