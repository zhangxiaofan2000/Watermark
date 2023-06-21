import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def detect_tampering(original_image_path, watermark_image_path, output_image_path):
    # 打开原始图像、水印图像和篡改后的图像
    original_image = Image.open(original_image_path)
    watermark_image = Image.open(watermark_image_path)
    output_image = Image.open(output_image_path)

    # 提取原始图像的红色通道
    original_red_channel = np.array(original_image)[:, :, 0]

    # 提取水印图像的红色通道
    watermark_red_channel = np.array(watermark_image)[:, :, 0]

    # 提取篡改后图像的红色通道
    output_red_channel = np.array(output_image)[:, :, 0]

    # 计算红色通道差值
    diff = np.abs(output_red_channel - original_red_channel)

    # 提取水印位置
    watermark_indices = np.where(watermark_red_channel == 0)
    threshold=1e4
    # 检测篡改
    tampered_indices = np.where(diff[watermark_indices] > threshold)  # 使用合适的阈值

    if tampered_indices[0].size > 0:
        print("图像已篡改")
    else:
        print("图像未篡改")

# 调用函数进行篡改检测
detect_tampering("original.png", "watermark.png", "output.png")
