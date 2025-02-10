import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.linear_model import LinearRegression


# python 3.1/summary_histgram_ba.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.1'


def mid_log(x, y):
    return np.exp((np.log(x)+np.log(y))/2)


def main():
    
    # ms -> s
    M = 1000
    Ts = [100, 200, 400, 800, 1600]
    
    # raw data T+delta:[normal, reverse]
    data = {}
    data[0] = {}
    data[1] = {}
    data[0][100] = {50:[3, 4], 59:[7, 2], 71:[14, 4], 84:[15, 4]}
    data[1][100] = {119: [6, 13], 141:[2, 11], 168:[0, 4], 200:[0, 1]}
    data[0][200] = {113:[1, 1], 130:[2, 0], 150:[2, 3], 173:[13, 6]}
    data[1][200] = {231:[7, 9], 266:[3, 5], 307:[0, 2], 354:[0, 0]}
    data[0][400] = {261:[1, 0], 291:[0, 2], 323:[4, 2], 360:[6, 5]}
    data[1][400] = {445:[10, 10], 495:[5, 3], 550:[2, 2], 612:[1, 0]}
    data[0][800] = {615:[0, 3], 657:[3, 6], 702:[1, 11], 749:[6, 9]}
    data[1][800] = {854:[11, 8], 912:[3, 7], 974:[5, 0], 1040:[1, 2]}
    data[0][1600] = {1231:[1, 2], 1314:[2, 4], 1403:[4, 3], 1498:[4, 16]}
    data[1][1600] = {1708:[11, 5], 1824:[6, 3], 1948:[5, 2], 2080:[1, 1]}
    
    dl_minus = {}
    dl_plus = {}
    
    colors = ['c', 'm']
    for i, color in enumerate(colors):
        fig, axes = plt.subplots(3, 2, figsize=(8, 12))
        for T, ax in zip(Ts, axes.flat):
            data[i][T][T] = [15, 15]
            keys = []
            values = []
            flg = True
            for key, value in sorted(data[i][T].items()):
                prob = sum(value) / 60
                keys.append(key)
                values.append(prob)
                if flg and i == 0 and prob > 0.25:
                    t_dl = np.exp((0.25 - values[-2]) * (np.log(keys[-1]) - np.log(keys[-2])) / (values[-1] - values[-2]) + np.log(keys[-2]))
                    dl_minus[mid_log(T-t_dl, T)] = T - t_dl
                    flg = False
                if flg and i == 1 and prob < 0.25:
                    t_dl = np.exp((0.25 - values[-2]) * (np.log(keys[-1]) - np.log(keys[-2])) / (values[-1] - values[-2]) + np.log(keys[-2]))
                    dl_minus[mid_log(T, T+t_dl)] = T + t_dl
                    flg = False
            pos = np.arange(len(keys))
            ax.bar(list(pos), values, width=1.0, color=color, edgecolor='black')
            ax.set_xticks(pos, keys)
            ax.set_ylim(0, 0.55)
            ax.set_xlabel(r'間隔 $T\times\alpha$ [ms]')
            ax.set_ylabel(r'誤答率 $P(T\times\alpha)$')
            ax.set_title(f'T={T}ms')
        fig.delaxes(axes.flat[-1])
        plt.tight_layout()
        plt.savefig(os.path.join(IMGDIR, f'histgram_{i}.png'))
        plt.show()
        

if __name__ == '__main__':
    main()