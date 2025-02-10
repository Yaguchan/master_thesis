import os
import math
import japanize_matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scipy.optimize import curve_fit


# python 3.3/dl_speech_all.py
OUTPUTDIR = '/Users/user/Desktop/授業/lab/資料/知覚実験3/output_v3'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def tone():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # output data
    
    # test
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    max_deltas = [400, 400, 400, 400, 400, 400, 800]
    wavlens = [1000, 1500]
    N = 9
    NA = 1e10
    
    # output list
    output_dict = {}
    for P in Ps:
        output_dict[P] = []
        
    names = os.listdir(OUTPUTDIR)
    names = [name for name in names if name != '.DS_Store']
    for name in names:
        namedir = os.path.join(OUTPUTDIR, name)
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                if wavlen == 2000: continue
                if delta == -1: delta = NA
                output_dict[P].append(delta)
    
    # cal dl
    def sigmoid(x, a, b):
        return 1 / (1 + np.exp(-(a * np.log(x) + b)))
    plt.figure(figsize=(6, 6))
    all_deltas = []
    for P, max_delta in zip(Ps, max_deltas):
        deltas = []
        for j in range(N):
            deltas.append(max_delta/(math.sqrt(2)**j))
        all_deltas.append(sorted(deltas))
    dls = []
    for P, deltas in zip(Ps, all_deltas):
        # 確率
        count = Counter(output_dict[P])
        cumulative_count = 0
        cumulative_counts = {}
        total_count = sum(count.values())
        for value in sorted(deltas):
            cumulative_count += count.get(value, 0)
            cumulative_counts[value] = cumulative_count
        # probs = {k: v / total_count for k, v in cumulative_counts.items()}
        probs = [v / total_count for k, v in cumulative_counts.items()]
        data = {
            "x": deltas[:-1],
            "p": probs[:-1]#.values()
        }
        df = pd.DataFrame(data)
        popt, pcov = curve_fit(sigmoid, df['x'], df['p'], p0=[-1, np.log(np.median(df['x']))])
        a, b = popt
        x_target = np.exp(-b/a)
        dls.append(x_target)
    print(dls)
    plt.plot(Ps, dls, marker='o', linestyle='-', label='speech all')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlim(10, 1000)
    plt.ylim(40, 300)
    plt.xlabel('基準値 $\it{T}$ [ms]', fontsize=15)
    # plt.xlabel('Interval $\it{T}$ [ms]', fontsize=15)
    plt.ylabel('弁別閾 $\Delta\it{T}_{DL}$ [ms]', fontsize=15)
    # plt.ylabel('Discrimination Threshold $\Delta\it{T}_{DL}$ [ms]', fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    # plt.legend(fontsize=10, title="Signal $\it{S}$ / Short・Long / Signal Duration $\it{D}$")
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'dl_speech_all.png'))
    plt.show()


if __name__ == "__main__":
    tone()