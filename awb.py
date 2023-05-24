import numpy as np 
import cv2

src0 = cv2.imread("xiaomi.png")
src = src0.astype(np.uint16)    # 调整一下数据类型，防止算术运算溢出

# 求出各个颜色分量的平均值
b_ave = np.mean(src[:, :, 0])
g_ave = np.mean(src[:, :, 1])
r_ave = np.mean(src[:, :, 2])

# 各个颜色分量的最大值
b_max = np.max(src[:, :, 0])
g_max = np.max(src[:, :, 1])
r_max = np.max(src[:, :, 2])

# 根据QCGP公式求出系数
k_ave = (b_ave + g_ave + r_ave)/3
k_max = (b_max + g_max + r_max)/3
k_matrix = np.mat([[k_ave], [k_max]])

# 通过矩阵求出B通道的转换矩阵，并计算出新图的B通道
b_coefficient_matrix = np.mat([[b_ave * b_ave, b_ave],
                               [b_max * b_max, b_max]])
b_conversion_matrix = b_coefficient_matrix.I * k_matrix

b = (src[:, :, 0]).transpose()
bb = (src[:, :, 0] * src[:, :, 0]).transpose()
b = np.stack((bb, b), axis=0).transpose()
b_des = np.dot(b, np.array(b_conversion_matrix))
b_des = b_des.astype(np.uint8).reshape([3880, 5184])

# 通过矩阵求出G通道的转换矩阵，并计算出新图的G通道
g_coefficient_matrix = np.mat([[g_ave * g_ave, g_ave],
                               [g_max * g_max, g_max]])
g_conversion_matrix = g_coefficient_matrix.I * k_matrix

g = (src[:, :, 1]).transpose()
gg = (src[:, :, 1] * src[:, :, 1]).transpose()
g = np.stack((gg, g), axis=0).transpose()
g_des = np.dot(g, np.array(g_conversion_matrix))
g_des = g_des.astype(np.uint8).reshape([3880, 5184])

# 通过矩阵求出R通道的转换矩阵，并计算出新图的R通道
r_coefficient_matrix = np.mat([[r_ave * r_ave, r_ave],
                               [r_max * r_max, r_max]])
r_conversion_matrix = r_coefficient_matrix.I * k_matrix

r = (src[:, :, 2]).transpose()
rr = (src[:, :, 2] * src[:, :, 2]).transpose()
r = np.stack((rr, r), axis=0).transpose()
r_des = np.dot(r, np.array(r_conversion_matrix))
r_des = r_des.astype(np.uint8).reshape([3880, 5184])

# 用一个新的矩阵接受新的图片，注意数据类型要和原图一致
src1 = np.zeros(src.shape).astype(np.uint8)
src1[:, :, 0] = b_des
src1[:, :, 1] = g_des
src1[:, :, 2] = r_des

# 显示图片
img = np.hstack([src0, src1])
cv2.imwrite("GW_Balance.jpg", img)