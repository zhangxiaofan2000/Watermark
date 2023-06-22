import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from detect_tampering import detect_tampering

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("水印应用")
        self.geometry("1050x550")
        # 图片路径变量
        self.original_image_path = str()
        self.watermark_image_path = str()
        self.output_image_path = str()
        self.tampering_image_path = str()
        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 创建按钮区域框架
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP)

        # 原始图片上传按钮
        self.original_image_button = tk.Button(
            button_frame, text="上传图片", command=self.upload_original_image)
        self.original_image_button.pack(side=tk.LEFT)

        # 水印图片上传按钮
        self.watermark_image_button = tk.Button(
            button_frame, text="上传水印图片", command=self.upload_watermark_image)
        self.watermark_image_button.pack(side=tk.LEFT)

        # 添加水印按钮
        self.add_watermark_button = tk.Button(
            button_frame, text="添加水印", command=self.add_watermark)
        self.add_watermark_button.pack(side=tk.LEFT)

        # 检测水印按钮
        self.detect_watermark_button = tk.Button(
            button_frame, text="检测水印", command=self.detect_watermark)
        self.detect_watermark_button.pack(side=tk.LEFT)

        # 上传被篡改图像
        self.add_tampering_button = tk.Button(
            button_frame, text="上传被篡改图像", command=self.upload_tampering_image)
        self.add_tampering_button.pack(side=tk.LEFT)

        # 篡改位置检测
        self.detect_tampering_button = tk.Button(
            button_frame, text="篡改位置检测", command=self.detect_tampering_button)
        self.detect_tampering_button.pack(side=tk.LEFT)

        # 原始图片展示区域
        self.original_image_label = tk.Label(self, background="#808080")
        self.original_image_label.place(width=200, height=200, y=50, x=50)
        original_image_text = tk.Label(self, text="原始图片")
        original_image_text.place(x=50, y=250)

        # 水印图片展示区域
        self.watermark_image_label = tk.Label(self, background="#808080")
        self.watermark_image_label.place(width=200, height=200, y=50, x=300)
        watermark_image_text = tk.Label(self, text="水印图片")
        watermark_image_text.place(x=300, y=250)


        # 添加水印结果展示区域
        self.output_image_label = tk.Label(self, background="#808080")
        self.output_image_label.place(width=200, height=200, y=50, x=550)
        output_image_text = tk.Label(self, text="水印结果")
        output_image_text.place(x=550, y=250)

        # 篡改图像展示区域
        self.tampering_image_label = tk.Label(self, background="#808080")
        self.tampering_image_label.place(width=200, height=200, y=50, x=800)
        tampering_image_text = tk.Label(self, text="篡改图像")
        tampering_image_text.place(x=800, y=250)


        # 原始图片频域图展示区域
        self.original_image_freq_label = tk.Label(self, background="#808080")
        self.original_image_freq_label.place(width=200, height=200, y=300, x=50)
        original_image_freq_text = tk.Label(self, text="原始图片频域图")
        original_image_freq_text.place(x=50, y=500)

        # 水印检测图展示区域
        self.watermark_detection_label = tk.Label(self, background="#808080")
        self.watermark_detection_label.place(width=200, height=200, y=300, x=300)
        watermark_detection_text = tk.Label(self, text="水印检测图")
        watermark_detection_text.place(x=300, y=500)

        # 位置检测图展示区域
        self.location_detection_label = tk.Label(self, background="#808080")
        self.location_detection_label.place(width=200, height=200, y=300, x=550)
        location_detection_text = tk.Label(self, text="位置检测图")
        location_detection_text.place(x=550, y=500)

    def upload_original_image(self):
        # 选择原始图片文件
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

        self.original_image_path = file_path
        self.show_image_path(self.original_image_label, file_path)
        original_image = Image.open(file_path)
        red_channel = np.array(original_image)[:, :, 0]
        fourier_transform = np.fft.fft2(red_channel)
        shifted_transform = np.fft.fftshift(fourier_transform)
        # 计算幅度谱（绝对值）
        magnitude_spectrum = np.abs(shifted_transform)
        # 对幅度谱进行对数变换
        log_magnitude_spectrum = np.log(1 + magnitude_spectrum)
        # 将幅度谱归一化到0-255范围内
        normalized_spectrum = (255 * (log_magnitude_spectrum - np.min(log_magnitude_spectrum)) /
                               (np.max(log_magnitude_spectrum) - np.min(log_magnitude_spectrum)))

        # 将归一化后的幅度谱转换为灰度图像数据类型
        gray_image = normalized_spectrum.astype(np.uint8)
        # 创建灰度图像对象
        gray_image_obj = Image.fromarray(gray_image, mode='L')
        self.show_image(self.original_image_freq_label,gray_image_obj )

    def upload_watermark_image(self):
        # 选择水印图片文件
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        self.watermark_image_path= file_path
        self.show_image_path(self.watermark_image_label, file_path)


    def add_watermark(self):
        # 获取图片路径
        original_image_path = self.original_image_path.get()
        watermark_image_path = self.watermark_image_path.get()
        if original_image_path and watermark_image_path:
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
            self.result_image = Image.fromarray(output_image)
            self.result_image.save("output.png")

            # 显示添加水印后的结果图片
            self.show_image(self.output_image_label, self.result_image)

    def detect_watermark(self):
        # 加载输出图像
        output_image = self.result_image
        output_array = np.array(output_image)
        # 提取红色通道
        red_channel = output_array[:, :, 0]
        # 进行傅里叶变换和频率中心化
        fourier_transform = np.fft.fft2(red_channel)
        shifted_transform = np.fft.fftshift(fourier_transform)
        # 计算频域图像的幅度谱
        magnitude_spectrum = np.abs(shifted_transform)
        # 对幅度谱进行对数变换
        log_magnitude_spectrum = np.log(1 + magnitude_spectrum)
        # 将幅度谱归一化到0-255范围内
        normalized_spectrum = (255 * (log_magnitude_spectrum - np.min(log_magnitude_spectrum)) /
                               (np.max(log_magnitude_spectrum) - np.min(log_magnitude_spectrum)))
        # 将归一化后的幅度谱转换为灰度图像数据类型
        gray_image = normalized_spectrum.astype(np.uint8)
        # 创建灰度图像对象
        gray_image_obj = Image.fromarray(gray_image, mode='L')
        self.show_image(self.watermark_detection_label, gray_image_obj)
    def detect_tampering_button(self):
        detect_tampering_obj  = detect_tampering()
        # 调用函数进行篡改检测和区域定位
        result_image = detect_tampering_obj.detect_tampering("output.png",self.tampering_image_path)
        cv2.imwrite("result_image.png", result_image)
        self.show_image_path(self.location_detection_label, "result_image.png")


    def upload_tampering_image(self):
        # 选择被篡改图片文件
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

        self.tampering_image_path= file_path
        self.show_image_path(self.tampering_image_label, file_path)


    def show_image_path(self, label, image_path):
        # 打开图片并调整大小
        image = Image.open(image_path)
        # 原始宽度和高度
        width, height = image.size
        # 新的宽度（设定为200）
        new_width = 200
        # 计算新的高度，按比例缩放
        new_height = int(height * (new_width / width))
        # 调整图像大小
        image = image.resize((new_width, new_height))
        # 将图片转换为Tkinter可用的格式
        tk_image = ImageTk.PhotoImage(image)
        # 显示图片
        label.configure(image=tk_image)
        label.image = tk_image

    def show_image(self, label, image):
        # 原始宽度和高度
        width, height = image.size
        # 新的宽度（设定为200）
        new_width = 200
        # 计算新的高度，按比例缩放
        new_height = int(height * (new_width / width))
        # 调整图像大小
        image = image.resize((new_width, new_height))
        # 将图片转换为Tkinter可用的格式
        tk_image = ImageTk.PhotoImage(image)
        # 显示图片
        label.configure(image=tk_image)
        label.image = tk_image



if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
