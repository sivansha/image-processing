from PIL import Image
from timeit import Timer
import numpy as np
from matplotlib import pyplot as plt
import os

def main():
    debug=True
    rounds = 5

    images = [b"lena.png", b"northcap.png"]
    # dict with key quality and values [file_size,psnr]

    for img in images:
        time_res = [] # [quality, file size, compression time]
        time_res_optimized = []
        img_YCbCr = Image.open(b"./"+img).convert("YCbCr")

        for optimize in [True, False]:
            for i in range(100,0,-10):
                filename = b"./images/time_quailty_compare.jpeg"
                t = Timer(lambda: save_file(img_YCbCr, filename, i, optimize))
                time = t.timeit(number=rounds)
                size = os.path.getsize(filename)
                if optimize:
                    time_res_optimized.append([i, size, time])
                else:
                    time_res.append([i, size, time])
        plot_time(time_res_optimized, time_res, debug)


def plot_time(time_res_optimized, time_res, debug=False):
    time_res_optimized = np.array(time_res_optimized)
    time_res = np.array(time_res)
    res = time_res_optimized/time_res
    if debug:
        print(res.tolist())
        print(time_res.tolist())
        print(time_res_optimized.tolist())
    # red dashes, blue squares and green triangles
    fig, ax = plt.subplots()
    ax.plot(res[:,1], res[:,2],  'g^')

    ax.set_title('Relative Time cost to relative file size saved')
    plt.show()

def plot_res(quality_res, optimization='False'):
    N = len(quality_res)
    filesizes = [x[1] / 1024 for x in quality_res]
    psnrs = [x[2] for x in quality_res]

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    ax.set_ylabel('File size [KByte]')
    ax.yaxis.label.set_color('blue')
    ax.plot(ind, filesizes, 'b-', linewidth=2.0)
    if filesizes[0] > 1000:
        ax.set_ylim([0, 11700])
    else:
        ax.set_ylim([0, 230])

    ax2 = ax.twinx()
    ax2.bar(ind, psnrs, width, alpha=0.4, color='r')
    # add some text for labels, title and axes ticks
    ax2.set_ylabel('PSNR [dB]')
    ax2.yaxis.label.set_color('red')
    ax2.set_title('JPEG Compression, Opimization = ' + optimization)
    ax2.set_xticks(ind)
    ax2.set_xticklabels([x[0] for x in quality_res])
    ax2.set_xlabel('Quality [%]')
    ax2.set_ylim([0, 60])

    # second y axis

    plt.show()


def save_file(img,filename,quality_level, optimizebool):
    if optimizebool:
        img.save(filename, 'JPEG', quality=quality_level, optimize="a")
    else:
        img.save(filename, 'JPEG', quality=quality_level)


if __name__ == "__main__":
    main()
