import cv2
import numpy as np

import cv2
import numpy as np

def detect_tampering(original_image_path, watermark_image_path, tampered_image_path):
    # 加载原始图像、水印图像和篡改后的图像
    original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
    watermark_image = cv2.imread(watermark_image_path, cv2.IMREAD_GRAYSCALE)
    tampered_image = cv2.imread(tampered_image_path, cv2.IMREAD_GRAYSCALE)

    # 调整图像大小以匹配
    tampered_image = cv2.resize(tampered_image, (original_image.shape[1], original_image.shape[0]))

    # 计算原始图像的频域特征
    original_fft = np.fft.fft2(original_image)

    # 计算篡改后的图像的频域特征
    tampered_fft = np.fft.fft2(tampered_image)

    # 计算频域特征之间的差异
    diff = np.abs(original_fft - tampered_fft)

    # 设定阈值，判断差异是否超过阈值
    threshold = 1000

    # 检测篡改区域
    tampered_region = np.where(diff > threshold)

    # 在原始图像上绘制篡改区域
    result_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
    result_image[tampered_region] = [0, 0, 255]  # 篡改区域标记为红色

    # 显示结果图像并保存
    cv2.imshow("Tampered Regions", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("result_image.png", result_image)



# 调用函数进行篡改检测和区域定位
detect_tampering("output.png", "水印.jpg", "result.png")
