import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class WatermarkAdder:

    def add_watermark(self, original_image_path, watermark_image_path, output_image_path):
        # 打开原始图像和水印图像
        original_image = Image.open(original_image_path)
        watermark_image = Image.open(watermark_image_path)

        # 提取原始图像的红色通道
        red_channel = np.array(original_image)[:, :, 0]

        # 对红色通道进行傅里叶变换和频率中心化
        fourier_transform = np.fft.fft2(red_channel)
        shifted_transform = np.fft.fftshift(fourier_transform)

        # 将水印图像转换为灰度图像并提取出水印位置
        watermark_array = np.array(watermark_image.convert('L'))
        watermark_indices = np.where(watermark_array == 0)

        # 在中心化的傅里叶变换结果上标记水印位置
        marked_transform = np.copy(shifted_transform)
        marked_transform[watermark_indices[0] + 10, watermark_indices[1] + 10] = 1

        # 对标记了水印的傅里叶变换结果进行逆变换得到水印图像
        marked_image = np.fft.ifft2(np.fft.ifftshift(marked_transform))
        marked_image = np.abs(marked_image)

        # 将水印图像与原始图像的彩色通道合并
        output_image = np.array(original_image)
        output_image[:, :, 0] = marked_image

        # 保存最后添加水印的彩色图片
        result_image = Image.fromarray(output_image)
        result_image.save(output_image_path)

    def extract_watermark(self, marked_image_path, watermark_image_path, output_image_path):
        # 打开标记了水印的图像和水印图像
        marked_image = Image.open(marked_image_path)
        watermark_image = Image.open(watermark_image_path)

        # 提取标记了水印的图像的红色通道
        marked_red_channel = np.array(marked_image)[:, :, 0]

        # 对标记了水印的红色通道进行傅里叶变换和频率中心化
        marked_transform = np.fft.fft2(marked_red_channel)
        shifted_transform = np.fft.fftshift(marked_transform)

        # 将水印图像转换为灰度图像并提取出水印位置
        watermark_array = np.array(watermark_image.convert('L'))
        watermark_indices = np.where(watermark_array == 0)

        # 将水印位置置为0，恢复原始的中心化的傅里叶变换结果
        restored_transform = np.copy(shifted_transform)
        restored_transform[watermark_indices[0] + 10, watermark_indices[1] + 10] = 1

        # 对恢复的中心化的傅里叶变换结果进行逆变换得到提取的水印图像
        restored_image = np.fft.ifft2(np.fft.ifftshift(restored_transform))
        restored_image = np.abs(restored_image)

        # 将提取的水印图像与标记了水印的图像的彩色通道合并
        output_image = np.array(marked_image)
        output_image[:, :, 0] = restored_image

        # 保存最后提取的水印图像
        result_image = Image.fromarray(output_image)
        result_image.save(output_image_path)

if __name__ == '__main__':
    # 创建WatermarkAdder类的实例
    watermark_adder = WatermarkAdder()
    # 调用类方法添加水印并保存结果彩色图像
    watermark_adder.add_watermark("原图.jpg", "水印.jpg", "output.png")
    # watermark_adder.extract_watermark("output.png", "水印.jpg", "output_wartermark.png")
