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
cd $MY_PATH/../images/q4/

for BITRATE in 2205k 876k 334k 139k 68k 36k
do
	echo "  [*] Converting video with bitrate = $BITRATE"
	mkdir cbr_bitrate_$BITRATE
	cd cbr_bitrate_$BITRATE
	#pass 1 
	# ffmpeg -y -i ../../big_buck_bunny.y4m -c:v libx264 -b:v 2204k -pass 1 -f mp4 /dev/null
	ffmpeg -y -i ../../../big_buck_bunny.y4m -threads 1 -c:v libx264 -pass 1 -b:v $BITRATE q4_a_cbr_2pass_$BITRATE_v2.mp4
	#ffmpeg -y -i ../../../big_buck_bunny.y4m -threads 1 -c:v libx264 -pass 1 -b:v $BITRATE -minrate $BITRATE -maxrate $BITRATE -bufsize `expr  $BITRATE / 24` q4_a_cbr_2pass_$BITRATE_v2.mp4
	ffmpeg -y -i ../../../big_buck_bunny.y4m -threads 1 -c:v libx264 -b:v $BITRATE -pass 2  q4_a_cbr_2pass_$BITRATE_v2.mp4
	#ffmpeg -y -i ../../../big_buck_bunny.y4m -threads 1 -c:v libx264 -b:v $BITRATE -pass 2 -minrate $BITRATE -maxrate $BITRATE -bufsize `expr  $BITRATE / 24` q4_a_cbr_2pass_$BITRATE_v2.mp4
	cd ../
done

echo "  [*] Convertion done."
