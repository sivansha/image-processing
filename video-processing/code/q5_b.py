#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

debug=False

file_names = ("bbb_br_2205.txt", "bbb_br_36.txt", "bbb_crf_30.txt", "bbb_br_334.txt", "bbb_crf_18.txt", "bbb_crf_48.txt")
#file_names = ("bbb_br_2205.txt", "bbb_crf_18.txt")

# numpy array to save the bitrates: [30 values for the first], [30 values for the second], ...
bitrates = []
i=0
for file_name in file_names:

    if debug: print(file_name)

    with open("../images/q5/crf-videos/"+file_name, 'r') as file:

        tmp_bitrate = 0
        sec = 0
        n=0
        for line in file.readlines():
            n+=1
            if line.startswith("stream"):
                continue

            tmp_bitrate += float(line.split("=")[2].split(" ")[0])
            if n == 23:
                bitrates.append([i, sec, tmp_bitrate])
                sec += 1
                tmp_bitrate =0
                n=0

    i += 1
print(bitrates)
bitrates = np.array(bitrates)
print(bitrates)



###
# Plotting
###

bitrates = bitrates.reshape(6, 31, 3)

ax = plt.subplot()
for i in range(0, 6, 1):
    print(i)

    if (i==0 or i==1 or i==3):
        ax.plot(bitrates[i, :, 1], bitrates[i, :, 2])
    else:
        ax.plot(bitrates[i, :, 1], bitrates[i, :, 2], ls="--")

    #ax.legend(file_names, loc='upper left')
ax.legend(("Target Bitrate 2205kb/s", "Target Bitrate 36kb/s", "CRF Value 30", "Target Bitrate 334kb/s", "CRF Value 18", "CRF Value 48"), loc="upper left")
#ax.margins(x=0.0, y=0.3)
ax.set(title='Bitrate during the video', ylabel='Bitrate [bit/second]', xlabel='Time [second]')

plt.savefig("../figures/q5_b_bitrate_over_time.png")
plt.show()