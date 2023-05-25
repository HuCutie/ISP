# File: awb.py
# Description: Auto White Balance (actually not Auto)
# Created: 2021/10/22 20:50
# Author: Qiu Jueqin (qiujueqin@gmail.com)


import numpy as np

from .basic_module import BasicModule
from .helpers import split_bayer, reconstruct_bayer

# 手动白平衡
# class AWB(BasicModule):
#     def __init__(self, cfg):
#         super().__init__(cfg)

#         self.r_gain = np.array(self.params.r_gain, dtype=np.uint32)  # x1024
#         self.gr_gain = np.array(self.params.gr_gain, dtype=np.uint32)  # x1024
#         self.gb_gain = np.array(self.params.gb_gain, dtype=np.uint32)  # x1024
#         self.b_gain = np.array(self.params.b_gain, dtype=np.uint32)  # x1024

#     def execute(self, data):
#         bayer = data['bayer'].astype(np.uint32)

#         sub_arrays = split_bayer(bayer, self.cfg.hardware.bayer_pattern)
#         gains = (self.r_gain, self.gr_gain, self.gb_gain, self.b_gain)

#         wb_sub_arrays = []
#         for sub_array, gain in zip(sub_arrays, gains):
#             wb_sub_arrays.append(
#                 np.right_shift(gain * sub_array, 10)
#             )

#         wb_bayer = reconstruct_bayer(wb_sub_arrays, self.cfg.hardware.bayer_pattern)
#         wb_bayer = np.clip(wb_bayer, 0, self.cfg.saturation_values.hdr)

#         data['bayer'] = wb_bayer.astype(np.uint16)

# 基于灰度世界的自动白平衡
class AWB(BasicModule):
    def __init__(self, cfg):
        super().__init__(cfg)

    def execute(self, data):
        bayer = data['bayer'].astype(np.float32)

        bayer_ch = split_bayer(bayer, self.cfg.hardware.bayer_pattern)
        
        means = [np.mean(ch) for ch in bayer_ch]
        mean_gray = np.mean(means)

        gains = [mean_gray / ch_mean for ch_mean in means]
        wb_ch = [np.multiply(ch, gain * 4) for ch, gain in zip(bayer_ch, gains)]

        wb_bayer = reconstruct_bayer(wb_ch, self.cfg.hardware.bayer_pattern)
        wb_bayer = np.clip(wb_bayer, 0, self.cfg.saturation_values.hdr)

        data['bayer'] = wb_bayer.astype(np.uint16)

# 基于白色块的自动白平衡
# class AWB(BasicModule):
#     def __init__(self, cfg):
#         super().__init__(cfg)

#     def execute(self, data):
#         bayer = data['bayer'].astype(np.float32)

#         bayer_ch = split_bayer(bayer, self.cfg.hardware.bayer_pattern)

#         # 计算最亮区域的平均值作为参考白色值
#         max_vals = [np.max(ch) for ch in bayer_ch]
#         ref_white = np.mean(max_vals)

#         gains = [ref_white / max_val for max_val in max_vals]
#         wb_ch = [np.multiply(ch, gain) for ch, gain in zip(bayer_ch, gains)]

#         wb_bayer = reconstruct_bayer(wb_ch, self.cfg.hardware.bayer_pattern)
#         wb_bayer = np.clip(wb_bayer, 0, self.cfg.saturation_values.hdr)

#         data['bayer'] = wb_bayer.astype(np.uint16)

# 基于动态阈值的自动白平衡
# class AWB(BasicModule):
#     def __init__(self, cfg):
#         super().__init__(cfg)

#     def execute(self, data):
#         bayer = data['bayer'].astype(np.float32)

#         bayer_ch = split_bayer(bayer, self.cfg.hardware.bayer_pattern)

#         # 计算每个通道的动态阈值
#         thresholds = [np.percentile(ch, 75) for ch in bayer_ch]

#         gains = [threshold / np.mean(ch) for ch, threshold in zip(bayer_ch, thresholds)]
#         print(gains)
#         wb_ch = [np.multiply(ch, gain) for ch, gain in zip(bayer_ch, gains)]

#         wb_bayer = reconstruct_bayer(wb_ch, self.cfg.hardware.bayer_pattern)
#         wb_bayer = np.clip(wb_bayer, 0, self.cfg.saturation_values.hdr)

#         data['bayer'] = wb_bayer.astype(np.uint16)

# 基于QCGP(QuadraticGW&PR)自动白平衡
# class AWB(BasicModule):
#     def __init__(self, cfg):
#         super().__init__(cfg)

#     def execute(self, data):
#         bayer = data['bayer'].astype(np.float32)

#         bayer_ch = split_bayer(bayer, self.cfg.hardware.bayer_pattern)
        
#         means_ch = [np.mean(ch) for ch in bayer_ch]
#         means_ch_max = [np.max(ch) for ch in bayer_ch]
        
#         means = np.mean(means_ch)
#         max = np.mean(means_ch_max)
#         k_matrix = np.mat([[means], [max]])
        
#         gains = []
#         for ch in bayer_ch:
#             mean = np.mean(ch)
#             max = np.max(ch)
#             coefficient_matrix = np.mat([[mean * mean, mean],
#                                          [max * max, max]])
#             conversion_matrix = coefficient_matrix.I * k_matrix
#             gains.append(conversion_matrix)
        
#         gains = np.array(gains)
#         for chs in bayer_ch:
#             for ch, gain in zip(chs, gains):
#                 a = np.array([ch * ch, ch])
#                 b = np.multiply(a, gain)
#         wb_ch = [np.multiply(np.array([ch * ch, ch]), gain) for chs in bayer_ch for ch, gain in zip(chs, gains)]

#         wb_bayer = reconstruct_bayer(wb_ch, self.cfg.hardware.bayer_pattern)
#         wb_bayer = np.clip(wb_bayer, 0, self.cfg.saturation_values.hdr)

#         data['bayer'] = wb_bayer.astype(np.uint16)