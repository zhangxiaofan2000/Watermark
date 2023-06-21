import numpy as np
from scipy.fftpack import dct
from PIL import Image

def exwmark(embimg):
    row, clm = embimg.shape[0], embimg.shape[1]
    m = embimg.copy()

    # 将图像划分为 8x8 的块
    x = []
    k = 0
    for ii in range(0, row, 8):
        for jj in range(0, clm, 8):
            z = m[ii:ii + 8, jj:jj + 8].copy()
            x.append(z)
            k += 1

    nn = x.copy()

    # 提取水印
    wm = []
    wm1 = []
    k = 0
    wmwd = []
    wmwd1 = []
    while k < 1024:
        for i in range(32):
            if k < len(x):
                kx = x[k].copy()  # 逐个提取块
                dkx = dct(dct(kx.T, norm='ortho').T, norm='ortho')  # 应用离散余弦变换
                nn[k] = dkx  # 保存变换后的DCT系数以便交叉检查

                # 修改此处以更改像素位置
                wm1.extend([dkx[7, 7]])  # 形成一个 32x32 元素的行

                # 无DCT的水印提取
                wmwd1.extend([kx[7, 7]])

            k += 1

        wm.append(wm1)
        wm1 = []  # 形成 32x32 的列
        wmwd.append(wmwd1)
        wmwd1 = []

    wm = np.array(wm)
    wm = np.where(wm >= 0, 0, 1)  # 二值化水印

    wm = wm.T

    img = Image.fromarray(wm.astype('uint8') * 255)
    img.save('wex.jpg')

# 示例用法
image = np.array(Image.open('output.png'))
exwmark(image)
