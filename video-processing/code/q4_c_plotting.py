#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

debug = True

high_array = np.load('../misc/q4_c_frame_contribution_highest.npy')
low_array = np.load('../misc/q4_c_frame_contribution_lowest.npy')

if debug:
    print(high_array)
    print(low_array)

N = 2
menMeans = (20, 35, 30, 35, 27)
womenMeans = (25, 32, 34, 20, 25)
menStd = (2, 3, 4, 1, 2)
womenStd = (3, 5, 2, 3, 3)

iFrames = (high_array[0, 0], low_array[0, 0])
pFrames = (high_array[1, 0], low_array[1, 0])
bFrames = (high_array[2, 0], low_array[2, 0])

ind = np.arange(N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence

p2 = plt.bar(ind, pFrames, width, color="orange")
p3 = plt.bar(ind, bFrames, width, color="red", bottom=pFrames)
p1 = plt.bar(ind, iFrames, width, color="blue", bottom=pFrames)

plt.ylabel('Amount of Frames')
plt.title('Amount of Frames by Type')
plt.xticks(ind, ('highest target bitrate', 'lowest target bitrate'))
plt.legend((p1[0], p2[0], p3[0]), ('I Frames', 'P Frames', 'B Frames'))

plt.savefig("../figures/q4_c_amount_of_frames.png")

#
# Pie chart for the highest target bitrate 
#

labels = 'I Frames ca. '+str(np.round_(high_array[0,1]/(1024), decimals=1))+' KB', 'P Frames ca. '+str(np.round_(high_array[1,1]/(1024), decimals=1))+' KB', 'B Frames ca. '+str(np.round_(high_array[2,1]/(1024), decimals=1))+' KB'
total_size = float(high_array [:, 1].sum())
sizes = [high_array[0,1]/total_size, high_array[1,1]/total_size, high_array[2,1]/total_size]
explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()

plt.title('Highest Target Bitrate File Size Distribution by Frametype')
pie = ax1.pie(sizes, explode=explode, colors=("blue", "orange", "red") , autopct='%1.1f%%',
        shadow=False, startangle=180)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend(pie[0], labels, loc="upper right", bbox_to_anchor = (1,1))

plt.savefig("../figures/q4_c_byte_size_distribution_high.png")

#
# Pie chart for the lowest target bitrate 
#
labels = 'I Frames ca. '+str(np.round_(low_array[0,1]/(1024), decimals=1))+' KB', 'P Frames ca. '+str(np.round_(low_array[1,1]/(1024), decimals=1))+' KB', 'B Frames ca. '+str(np.round_(low_array[2,1]/(1024), decimals=1))+' KB'
total_size = float(low_array [:, 1].sum())
sizes = [low_array[0,1]/total_size, low_array[1,1]/total_size, low_array[2,1]/total_size]
explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()

plt.title('Lowest Target Bitrate File Size Distribution by Frametype')
pie = ax1.pie(sizes, explode=explode, colors=("blue", "orange", "red") , autopct='%1.1f%%',
        shadow=False, startangle=180)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend(pie[0], labels, loc="upper right", bbox_to_anchor = (1,1))

plt.savefig("../figures/q4_c_byte_size_distribution_low.png")

plt.show()