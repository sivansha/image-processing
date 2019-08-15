import matplotlib.pyplot as plt
from pathlib import Path

files = ['ssim_18-2205.log', 'ssim_30-334.log', 'ssim_48-36.log']
ssim_av_per_sec_per_file = []

for file in files:
    p = Path(file)
    lines = p.read_text().splitlines()

    i = 1
    ssim_av = 0
    ssim_av_per_sec = []
    for line in lines:
        ssim_value = line.split(" ")[4].split(":")[1]

        ssim_av += float(ssim_value)
        i += 1
        if i % 24 == 0:
            ssim_av_per_sec.append(round((ssim_av/24), 6))
            ssim_value = 0
            ssim_av = 0

    ssim_av_per_sec_per_file.append(ssim_av_per_sec)

print(ssim_av_per_sec_per_file)

titles = ["VBR with CRF = 18 compared with CBR with Br 2205", "VBR with CRF = 30 compared with CBR with Br 334", "VBR with CRF = 48 compared with CBR with Br 36"]
i = 0
for ssim_av in ssim_av_per_sec_per_file:
    fig, ax = plt.subplots()
    ax.plot(ssim_av, color='lightblue', linewidth=3, marker="o")
    ax.set(title=titles[i],
           ylabel='SSIM value [decibels]',
           xlabel='time axis in seconds')
    #ax.xaxis.set(ticks=range(1,31, 1))
    #ax.set_xlim(left=1)
    plt.savefig('../../../images/q5/q5_' + str(i) + '_plot.png')
    plt.show()
    i += 1
