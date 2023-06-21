import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def add_watermark(original_image_path, watermark_image_path, output_image_path):
    # 打开原始图像和水印图像
    original_image = Image.open(original_image_path)
    watermark_image = Image.open(watermark_image_path)

    # 显示原始图像和水印图像
    fig, ax = plt.subplots(ncols=2)
    ax[0].imshow(original_image)
    ax[0].set_title("原始图像")
    ax[1].imshow(watermark_image)
    ax[1].set_title("水印图像")
    plt.show()

    # 提取原始图像的红色通道
    red_channel = np.array(original_image)[:, :, 0]

    # 显示原始图像和红色通道
    fig, ax = plt.subplots(ncols=2)
    ax[0].imshow(original_image)
    ax[0].set_title("原始图像")
    ax[1].imshow(red_channel, cmap='autumn')
    ax[1].set_title("红色通道")
    plt.show()

    # 对红色通道进行傅里叶变换和频率中心化
    fourier_transform = np.fft.fft2(red_channel)
    shifted_transform = np.fft.fftshift(fourier_transform)

    # 显示红色通道、傅里叶变换结果和中心化的傅里叶变换结果
    fig, ax = plt.subplots(ncols=3, sharey=True)
    ax[0].imshow(red_channel, cmap='autumn')
    ax[0].set_title("红色通道")
    ax[1].imshow(np.log(abs(fourier_transform)), cmap='gray')
    ax[1].set_title("傅里叶变换结果")
    ax[2].imshow(np.log(abs(shifted_transform)), cmap='gray')
    ax[2].set_title("中心化的傅里叶变换结果")
    plt.show()

    # 将水印图像转换为灰度图像并提取出水印位置
    watermark_array = np.array(watermark_image.convert('L'))
    watermark_indices = np.where(watermark_array == 0)

    # 在中心化的傅里叶变换结果上标记水印位置
    marked_transform = np.copy(shifted_transform)
    marked_transform[watermark_indices[0] + 10, watermark_indices[1] + 10] = 1

    # 显示中心化的傅里叶变换结果和标记了水印的傅里叶变换结果
    fig, ax = plt.subplots(ncols=2, sharey=True)
    ax[0].imshow(np.log(abs(shifted_transform)))
    ax[0].set_title("中心化的傅里叶变换结果")
    ax[1].imshow(np.log(abs(marked_transform)))
    ax[1].set_title("标记了水印的傅里叶变换结果")
    plt.show()

    # 对标记了水印的傅里叶变换结果进行逆变换得到水印图像
    marked_red_channel = abs(np.fft.ifft2(marked_transform))

    # 显示原始红色通道和提取出的水印图像
    fig, ax = plt.subplots(ncols=2, sharey=True)
    ax[0].imshow(red_channel, cmap='autumn')
    ax[0].set_title("原始红色通道")
    ax[1].imshow(marked_red_channel, cmap='autumn')
    ax[1].set_title("提取出的水印图像")
    plt.show()

    # 对提取出的水印图像进行傅里叶变换并计算对数幅值
    check_transform = np.fft.fft2(marked_red_channel)
    check_transform_log = np.log(abs(check_transform))

    # 显示水印图像的傅里叶变换结果和局部放大的结果
    fig, ax = plt.subplots(ncols=1)
    ax.imshow(check_transform_log)
    ax.set_title("水印图像的傅里叶变换结果")
    plt.show()

# 调用函数添加水印并保存结果图像
add_watermark("原图.jpg", "watermark.png", "output.png")
