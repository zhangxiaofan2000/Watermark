import cv2
import numpy as np
import matplotlib.pyplot as plt

# 添加水印到指定位置
def add_watermark(image, watermark, x, y):
    image_fft = np.fft.fft2(image)
    watermark_fft = np.fft.fft2(watermark)
    watermark_fft_shift = np.fft.fftshift(watermark_fft)

    # 在指定位置添加水印
    image_fft[y:y+watermark.shape[0], x:x+watermark.shape[1]] = watermark_fft_shift

    image_with_watermark = np.fft.ifftshift(image_fft)
    image_with_watermark = np.fft.ifft2(image_with_watermark)
    image_with_watermark = np.abs(image_with_watermark)

    return image_with_watermark

# 示例用法
image_path = 'test.png'
watermark_path = 'watermark.png'

# 读取图像和水印
image = cv2.imread(image_path)
watermark = cv2.imread(watermark_path)

# 添加水印到指定位置
image_with_watermark = add_watermark(image, watermark, 0, 0)

# 创建2x2的图像布局
fig, axs = plt.subplots(2, 2)

# 显示原图
axs[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axs[0, 0].set_title('Original Image')

# 显示水印图
axs[0, 1].imshow(cv2.cvtColor(watermark, cv2.COLOR_BGR2RGB))
axs[0, 1].set_title('Watermark')

# 显示添加水印的原图
axs[1, 0].imshow(cv2.cvtColor(image_with_watermark, cv2.COLOR_BGR2RGB))
axs[1, 0].set_title('Image with Watermark')

# 显示定位图（未实现）
axs[1, 1].axis('off')
axs[1, 1].set_title('Tampered Regions (Not Implemented)')

# 设置布局紧凑
plt.tight_layout()

# 显示图像
plt.show()
