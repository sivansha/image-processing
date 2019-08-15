#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

print("  [*] Plot of psnr ssim")
# video original	video reference	    PSNR	    SSIM
# VBR - CRF = 18	CBR – Br = 2205k	    44.971699	0.991189 (20.549530)
# VBR - CRF = 30	CBR – Br = 334k	    38.264819	0.972306 (15.576179)
# VBR - CRF = 48	CBR – Br = 36k	    31.667522	0.891086 (9.629159)

values_psnr = np.array([[18, 44.971699], [30, 38.264819], [48, 31.667522]])
values_ssim = np.array([[18, 0.991189], [30, 0.972306], [48, 0.891086]])

fig, ax = plt.subplots()
ax.plot(values_psnr[:, 0], values_psnr[:, 1], color='lightblue', linewidth=3, marker="o")
ax.set(title='PSNR value when comparing VBR and CBR video files',
       ylabel='PSNR value [decibels]',
       xlabel='CRF/Bitrate values of input video files')
ax.xaxis.set(ticks=[18, 30, 48])
ax.set_xticklabels(["crf-18/Br-2205k", "crf-30/Br-334k", "crf-48/Br-36k"])
ax.yaxis.set(ticks=values_psnr[:, 1])
plt.savefig('../images/q5/q5_a1_plot.png')
plt.show()

fig, ax = plt.subplots()
ax.plot(values_ssim[:, 0], values_ssim[:, 1], color='lightblue', linewidth=3, marker="o")
ax.set(title='SSIM value when comparing VBR and CBR video files',
       ylabel='SSIM value [decibels]',
       xlabel='CRF/Bitrate values of input video files')
ax.xaxis.set(ticks=[18, 30, 48])
ax.set_xticklabels(["crf-18/Br-2205k", "crf-30/Br-334k", "crf-48/Br-36k"])
ax.yaxis.set(ticks=values_ssim[:, 1])
plt.savefig('../images/q5/q5_a2_plot.png')
plt.show()
