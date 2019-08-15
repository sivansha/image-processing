#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt


def typeSwitch(tmp_type):
    if tmp_type.startswith("I"): return 0
    if tmp_type.startswith("P"): return 1
    if tmp_type.startswith("B"): return 2

#debug switch
debug=False


# ffprobe command to get frame output:
# ffprobe -show_frames -threads 1 cbr_bitrate_36k/q4_a_cbr_2pass_36k.mp4 > q4_d_lowest_bitrate_result.txt

# arrays to save the information about the frames
# [I-frame amount, I-frame size], [P-frame amount, P-frame size], [B-frame amount, B-frame size]

low_array = np.array([[0, 0], [0, 0], [0, 0]])
high_array = np.array([[0, 0], [0, 0], [0, 0]])

if debug:
    print(low_array)
    print(high_array)

round=0

for file_name in ["../images/q4/q4_d_highst_bitrate_result.txt","../images/q4/q4_d_lowest_bitrate_result.txt" ]:
    with open(file_name, 'r') as file:
        print ("counting "+file_name)
        content = file.readlines()
        if debug:
            print(content)
            print(type(content))

        for line in content:
            #pkt_size=846\n
            #pict_type=I\n
            if line.startswith("pkt_size="):
                tmp_size = float(line.split("=")[1])
            if line.startswith("pict_type="):
                tmp_type = line.split("=")[1]
                i = typeSwitch(tmp_type)

                if round == 0:
                    high_array[i, 0] = high_array[i, 0]+1
                    high_array[i, 1] = high_array[i, 1]+tmp_size

                if round == 1:
                    low_array[i, 0] = low_array[i, 0]+1
                    low_array[i, 1] = low_array[i, 1]+tmp_size


    round +=1
print(high_array)
print(low_array)
np.save('../misc/q4_c_frame_contribution_highest', high_array)
np.save('../misc/q4_c_frame_contribution_lowest', low_array)