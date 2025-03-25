import torch
import torch.nn as nn
from pytorch_wavelets import DWTForward

import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import torchvision
# GitHub地址 ：https://github.com/apple1986/HWD
# 论文地址：https://www.sciencedirect.com/science/article/pii/S0031320323005174
class Down_wt(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(Down_wt, self).__init__()
        self.wt = DWTForward(J=1, mode='zero', wave='haar') #mexh
        self.conv_bn_relu = nn.Sequential(
            nn.Conv2d(in_ch * 4, out_ch, kernel_size=1, stride=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

        self.conv_bn_relu2 = nn.Sequential(
            nn.Conv2d(in_ch * 4, out_ch, kernel_size=3, stride=1,padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

        self.conv_bn_relu3 = nn.Sequential(
            nn.Conv2d(in_ch * 4, out_ch, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

        self.mix = nn.Linear(3 * out_ch, out_ch)




    def forward(self, x):
        B, C, _, _ = x.shape

        yL, yH = self.wt(x)
        y_HL = yH[0][:, :, 0, ::]
        y_LH = yH[0][:, :, 1, ::]
        y_HH = yH[0][:, :, 2, ::]

        x = torch.cat([yL, y_HL, y_LH, y_HH], dim=1)
        x1 = self.conv_bn_relu(x)
        x1 = x1.reshape(B, C, -1)

        x2 = self.conv_bn_relu2(x)
        x2 = x2.reshape(B, C, -1)

        x3 = self.conv_bn_relu3(x)
        x3 = x3.reshape(B, C, -1)

        output = torch.concatenate([x1, x2, x3], dim=1)
        output = self.mix(output.permute(0, 2, 1)).permute(0, 2, 1)
        return output

def draw():
    pass
    # plt.figure(figsize=(20, 18))
    # plt.subplot(2, 2, 1)
    # img = x[0][0].cpu().numpy()
    # img = img.astype('float32')
    # img = (img - np.min(img)) / (np.max(img) - np.min(img))
    #
    # im = plt.imshow(img, cmap='Blues', interpolation='nearest')
    # cbar = plt.colorbar(im)  # 获取颜色条对象
    # cbar.set_label('Value Bar', fontsize=20, fontweight='bold')  # 给颜色条加上文本说明
    # plt.title('2D Input', fontsize=20, fontweight='bold')
    #
    # plt.subplot(2, 2, 2)
    # img_HL = y_HL[0][0].cpu().numpy()
    # img_HL = img_HL.astype('float32')
    # img_HL = (img_HL - np.min(img_HL)) / (np.max(img_HL) - np.min(img_HL))
    # plt.imshow(img_HL, cmap='Blues', interpolation='nearest')
    # plt.colorbar()  # 显示颜色条
    # plt.title('High-Low', fontsize=20, fontweight='bold')
    #
    # plt.subplot(2, 2, 3)
    # img_LH = y_HL[0][0].cpu().numpy()
    # img_LH = img_LH.astype('float32')
    # img_LH = (img_LH - np.min(img_LH)) / (np.max(img_LH) - np.min(img_LH))
    # plt.imshow(img_LH, cmap='Blues', interpolation='nearest')
    # plt.colorbar()  # 显示颜色条
    # plt.title('Low-High', fontsize=20, fontweight='bold')
    #
    # plt.subplot(2, 2, 4)
    # img_HH = y_HL[0][0].cpu().numpy()
    # img_HH = img_HH.astype('float32')
    # img_HH = (img_HH - np.min(img_HH)) / (np.max(img_HH) - np.min(img_HH))
    # plt.imshow(img_HH, cmap='Blues', interpolation='nearest')
    # plt.colorbar()  # 显示颜色条
    # plt.title('High-High', fontsize=20, fontweight='bold')
    #
    # plt.savefig('tmp.pdf', bbox_inches='tight', dpi=500)  # 保存成PDF放大后不失真（默认保存在了当前文件夹下）
    # plt.show()

    # 加一个文件夹

if __name__ == '__main__':
    block = Down_wt(64, 128)  # 输入通道数，输出通道数
    input = torch.rand(3, 64, 64, 64)  # 输入B C H W
    output = block(input)
    print(output.size())