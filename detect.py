import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 加载输出图像
output_image = Image.open("output.png")
output_array = np.array(output_image)

# 提取红色通道
red_channel = output_array[:, :, 0]

# 进行傅里叶变换和频率中心化
fourier_transform = np.fft.fft2(red_channel)
shifted_transform = np.fft.fftshift(fourier_transform)

# 计算频域图像的幅度谱
magnitude_spectrum = np.abs(shifted_transform)

# 可视化频域图像
plt.imshow(np.log(1 + magnitude_spectrum), cmap='gray')
plt.title('红色通道频域')
plt.show()
