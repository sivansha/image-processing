#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

print("  [*] Plot of average bitrate")
#2205k 876k 334k 139k 68k 36k
values = np.array([[18, 2205], [24, 876], [30, 334], [36, 139], [42, 68], [48, 36]])
np.save('../misc/q3_c_crf_and_bitrate_values', values)

#print (np.load('../misc/q3_c_crf_and_bitrate_values.npy'))

fig, ax = plt.subplots()

ax.plot(values[:, 0], values[:,1], color='lightblue', linewidth=3, marker="o")

ax.set(title='Bitrate over CRF values Plot',
       ylabel='Bitrate [kb/s]',
       xlabel='CRF value')

ax.xaxis.set(ticks=values[:, 0])

for i,j in values:
    ax.annotate(str(j), xy=(i+0.3, j))

plt.savefig('../figures/q3_d_plot.png')
plt.show()
