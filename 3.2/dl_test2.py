import os
import math
import japanize_matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scipy.optimize import curve_fit


# python 3.2/dl_test2.py
OUTPUTDIR = '/Users/user/Desktop/授業/lab/資料/知覚実験/output_/test2'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.2'


def tone():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # output data
    names = os.listdir(OUTPUTDIR)
    names = [name for name in names if name != '.DS_Store']
    
    # test
    Ps = [12.5, 25, 50, 100]
    max_deltas = [200, 200, 200, 200]
    wavlens = [1000, 1500, 2000]
    N = 9
    M = 800
    NA = 1e10
    
    ## output list
    output_before_dict = {}
    for wavlen in wavlens:
        output_before_dict[wavlen] = {}
        for P in Ps:
            output_before_dict[wavlen][P] = []
    
    for name in names:
        namedir = os.path.join(OUTPUTDIR, name)
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                if delta == -1: delta = NA
                output_before_dict[wavlen][P].append(delta)
    
    list_all_deltas = []
    all_deltas = []
    for P, max_delta in zip(Ps, max_deltas):
        deltas = []
        for i in range(N): 
            deltas.append(max_delta/(math.sqrt(2)**i))
        all_deltas.append(sorted(deltas))
    
    # cal dl
    def sigmoid(x, a, b):
        return 1 / (1 + np.exp(-(a * np.log(x) + b)))
    colors = ['#9999FF', '#3333FF', '#000099']
    plt.figure(figsize=(6, 6))
    for wavlen, color in zip(wavlens, colors):
        dls = []
        adjusted_dls = []
        output_dict = output_before_dict[wavlen]
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
            # print(x_target)
            dls.append(x_target)
            adjusted_dls.append(x_target-P)
        # print(sl, wavlen, np.average(dls))
        print(dls)
        label_name = '$\it{T}-\Delta\it{T}$'
        plt.plot(Ps, dls, marker='x', linestyle='--', color=color, label=f'{wavlen}ms'+'$(\Delta\it{T})$')
        plt.plot(Ps, adjusted_dls, marker='+', linestyle='dotted', color=color, label=f'{wavlen}ms'+'$(\Delta\it{T}-T)$')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlim(10, 1000)
    plt.ylim(10, 400)
    plt.xlabel('基準値 $\it{T}$ [ms]', fontsize=15)
    plt.ylabel('弁別閾 $\Delta\it{T}_{DL}$ [ms]', fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    plt.legend(fontsize=10, title="信号長D")
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'dl_test2.png'))
    plt.show()


if __name__ == "__main__":
    tone()