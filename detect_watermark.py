import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def detect_watermark(original_image_path, watermark_image_path):
    # 打开原始图像和水印图像
    original_image = Image.open(original_image_path).convert("L")
    watermark_image = Image.open(watermark_image_path).convert("L")

    # 对原始图像进行傅里叶变换和频率中心化
    fourier_transform = np.fft.fft2(original_image)
    shifted_transform = np.fft.fftshift(fourier_transform)

    # 将水印图像转换为灰度图像并提取出水印位置
    watermark_array = np.array(watermark_image)
    watermark_indices = np.where(watermark_array == 0)

    # 在中心化的傅里叶变换结果上标记水印位置
    marked_transform = np.copy(shifted_transform)
    marked_transform[watermark_indices] = 1

    # 检测水印位置是否存在频域水印
    if np.any(marked_transform[watermark_indices] == 1):
        print("图像的水印位置存在频域水印")
    else:
        print("图像的水印位置不存在频域水印")

# 调用函数进行水印检测
detect_watermark("test.png", "watermark.png")
