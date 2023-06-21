import cv2
import numpy as np
import matplotlib.pyplot as plt
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 添加水印到指定位置


def add_watermark(image, watermark):
    # 获取原图和水印的尺寸
    image_h, image_w, _ = image.shape
    watermark_h, watermark_w, watermark_channels = watermark.shape

    # 创建一个与原图相同大小的透明图像
    transparent_image = np.zeros((image_h, image_w, 3), dtype=np.uint8)
    transparent_image[:, :] = (0, 0, 0)  # 设置为完全透明的黑色

    # 计算水印放置的位置
    x = image_w - watermark_w - 10
    y = image_h - watermark_h - 10

    if watermark_channels == 4:  # 如果水印具有透明通道
        watermark_alpha = watermark[:, :, 3]  # 提取透明通道
        # 将水印的 RGB 通道乘以透明度，并将结果复制到透明图像的指定位置
        transparent_image[y:y+watermark_h, x:x+watermark_w, :] = watermark[:, :, :3] * (watermark_alpha / 255.0)
    else:
        # 将水印复制到透明图像的指定位置
        transparent_image[y:y+watermark_h, x:x+watermark_w] = watermark

    # 将透明图像与原图相加
    watermarked_image = cv2.add(image, transparent_image)

    return watermarked_image







# 检测水印篡改
def detect_tampering(image_with_watermark):
    # 将图像转换为灰度图像
    gray_image = cv2.cvtColor(image_with_watermark, cv2.COLOR_BGR2GRAY)

    # 应用离散傅立叶变换
    dft = np.fft.fft2(gray_image)
    dft_shift = np.fft.fftshift(dft)

    # 设置高频区域（水印区域）为0
    rows, cols = gray_image.shape
    center_row, center_col = rows // 2, cols // 2
    dft_shift[center_row - 50:center_row + 50, center_col - 50:center_col + 50] = 0

    # 应用逆傅立叶变换
    dft_ishift = np.fft.ifftshift(dft_shift)
    tampered_image = np.abs(np.fft.ifft2(dft_ishift))

    # 计算幅值谱
    magnitude_spectrum = 20 * np.log(np.abs(dft_shift))

    return tampered_image, magnitude_spectrum


# 定位被篡改的区域
def locate_tampered_regions(image, tampered_regions):
    contours, _ = cv2.findContours(tampered_regions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tampered_rectangles = []

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        tampered_rectangles.append((x, y, x+w, y+h))

    return tampered_rectangles


# 示例用法
image_path = 'test.png'
watermark_path = 'watermark.png'

# 读取图像和水印
image = cv2.imread(image_path)
watermark = cv2.imread(watermark_path)

# 添加水印到指定位置
image_with_watermark = add_watermark(image, watermark)

# 检测水印篡改
# tampered_image, tampered_regions = detect_tampering(image_with_watermark)

# 定位被篡改的区域
# tampered_rectangles = locate_tampered_regions(image, tampered_regions)

# 创建2x2的图像布局
fig, axs = plt.subplots(2, 2)

# 显示原图
axs[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axs[0, 0].set_title('原始图像')

# 显示水印图
axs[0, 1].imshow(watermark)
axs[0, 1].set_title('水印')

# 显示添加水印的原图
image_with_watermark = image_with_watermark.astype(np.uint8)
axs[1, 0].imshow(cv2.cvtColor(image_with_watermark, cv2.COLOR_BGR2RGB))
axs[1, 0].set_title('添加水印的图像')

# 显示定位图
# axs[1, 1].imshow(tampered_regions, cmap='gray')
axs[1, 1].set_title('篡改区域')

# 设置布局紧凑
plt.tight_layout()

# 显示图像
plt.show()
