#!/bin/bash

#welcome message
printf "  [*] This script is going to convert the big buck bunny movie as needed for q3 of the multimedia lab sheet 2\n"

# saving path where the script is saved
MY_PATH="`dirname \"$0\"`"

#checking in relativ location from the script if the video is downloaded
if [ ! -f $MY_PATH/../big_buck_bunny.y4m ]; then
	echo "[!!!] File not found!"
	echo "  [*] Please download the video file."
	echo "  [*] Use the original name: big_buck_bunny.y4m"
	echo "  [*] Save the file in multimedia/sheet2/"
	echo "  [*] You can download it from here: https://service.inet.tu-berlin.de/owncloud/index.php/s/oVnj8eoJdL8ySGU"
	exit 1
fi
echo "  [*] Video found"

# checking wheter ffmpeg is installed
FFMPEG_PATH="`command -v ffmpeg`"
if [ -z "$FFMPEG_PATH" ];then
	echo "[!!!] ffmpeg not found"
	echo "  [*] Please install ffmpeg before continuing"
	exit 1
fi
echo "  [*] ffmpeg found"

#conversion of the videos

for CRF_VALUE in 18 24 30 36 42 48
do
	echo "  [*] Converting video with crf value = $CRF_VALUE"
	ffmpeg -i $MY_PATH/../big_buck_bunny.y4m -threads 1 -c:v libx264 -crf $CRF_VALUE $MY_PATH/../images/q3/big_buck_bunny_crf_$CRF_VALUE.mp4
done

echo "  [*] Convertion done."
