import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

from watermark_adder import WatermarkAdder

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("水印应用")
        self.geometry("800x400")

        # 图片路径变量
        self.original_image_path = tk.StringVar()
        self.watermark_image_path = tk.StringVar()
        self.output_image_path = tk.StringVar()

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 创建按钮区域框架
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP)

        # 原始图片上传按钮
        self.original_image_button = tk.Button(
            button_frame, text="上传原始图片", command=self.upload_original_image)
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

        # 原始图片展示区域
        self.original_image_label = tk.Label(self)
        self.original_image_label.pack(side=tk.LEFT)

        # 水印图片展示区域
        self.watermark_image_label = tk.Label(self)
        self.watermark_image_label.pack(side=tk.LEFT)

        # 添加水印结果展示区域
        self.output_image_label = tk.Label(self)
        self.output_image_label.pack(side=tk.LEFT)

    def upload_original_image(self):
        # 选择原始图片文件
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        self.original_image_path.set(file_path)
        self.show_image(self.original_image_label, file_path)

    def upload_watermark_image(self):
        # 选择水印图片文件
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        self.watermark_image_path.set(file_path)
        self.show_image(self.watermark_image_label, file_path)

    def add_watermark(self):
        # 获取图片路径
        original_image_path = self.original_image_path.get()
        watermark_image_path = self.watermark_image_path.get()

        if original_image_path and watermark_image_path:
            # 生成输出图片路径
            output_image_path = "output.png"

            watermark_adder = WatermarkAdder()
            # 调用添加水印函数
            watermark_adder.add_watermark(original_image_path, watermark_image_path, output_image_path)

            # 显示添加水印后的结果图片
            self.show_image(self.output_image_label, output_image_path)

    def detect_watermark(self):
        # TODO: 实现检测水印的功能
        pass

    def show_image(self, label, image_path):
        # 打开图片并调整大小
        image = Image.open(image_path)
        image = image.resize((200, 200))

        # 将图片转换为Tkinter可用的格式
        tk_image = ImageTk.PhotoImage(image)

        # 显示图片
        label.configure(image=tk_image)
        label.image = tk_image


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
