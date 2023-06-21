import cv2
import numpy as np

def detect_watermark(image_path, watermark_path):
    # 加载原始图像和水印图像
    image = cv2.imread(image_path, 0)
    watermark = cv2.imread(watermark_path, 0)

    # 对原始图像和水印图像进行傅里叶变换
    image_fft = np.fft.fft2(image)
    watermark_fft = np.fft.fft2(watermark)

    # 计算原始图像和水印图像的频域差异
    diff = np.abs(image_fft - watermark_fft)

    # 设置阈值来判断是否含有水印
    threshold = 1e4

    # 判断水印是否存在
    if np.sum(diff) > threshold:
        print("图像中可能含有频域水印")
    else:
        print("图像中不含频域水印")

# 调用函数进行水印检测
detect_watermark("output.png", "watermark.png")
