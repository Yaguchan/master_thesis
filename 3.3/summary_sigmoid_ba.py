import os
import math
import japanize_matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scipy.optimize import curve_fit


# python 3.3/summary_sigmoid_ba.py
OUTPUTDIR = '/Users/user/Desktop/授業/lab/資料/知覚実験2/output_v2'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def main():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # output data
    names = os.listdir(OUTPUTDIR)
    names = [name for name in names if name != '.DS_Store']
    
    # test
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    max_deltas = [200, 200, 200, 200, 200, 400, 800]
    # max_deltas = [400, 400, 400, 400, 400, 400, 800]
    N = 9
    M = 1e10
    MIN = 1
    MAX = 1000
    
    # linear/log
    x_range = np.linspace(MIN, MAX, (MAX-MIN)*1+1)
    
    # output list
    output_before_dict = {}
    output_after_dict = {}
    for P in Ps:
        output_before_dict[P] = []
        output_after_dict[P] = []
    
    for name in names:
        namedir = os.path.join(OUTPUTDIR, name)
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                if delta == -1: delta = M
                if sl == 0:
                    output_before_dict[P].append(delta)
                else:
                    output_after_dict[P].append(delta)
    
    all_deltas = []
    for P, max_delta in zip(Ps, max_deltas):
        deltas = []
        for i in range(N): 
            deltas.append(max_delta/(math.sqrt(2)**i))
        all_deltas.append(sorted(deltas))
    
    # cal dl
    def sigmoid(x, a, b):
        return 1 / (1 + np.exp(-(a * np.log(x) + b)))
    output_dicts = [output_before_dict, output_after_dict]
    colors = [['c', 'b'], ['m', 'r']]
    for sl, (output_dict, color) in enumerate(zip(output_dicts, colors)):
        raw_ps = []
        ps = []
        dls = []
        fig, axes = plt.subplots(4, 2, figsize=(8, 12))
        for P, deltas, ax in zip(Ps, all_deltas, axes.flat):
            # 確率
            count = Counter(output_dict[P])
            cumulative_count = 0
            cumulative_counts = {}
            total_count = sum(count.values())
            for value in sorted(deltas):
                cumulative_count += count.get(value, 0)
                cumulative_counts[value] = cumulative_count
            probs = {k: v / total_count for k, v in cumulative_counts.items()}
            data = {
                "x": deltas,
                "p": probs.values()
            }
            raw_ps.append(list(probs.values()))
            df = pd.DataFrame(data)
            popt, pcov = curve_fit(sigmoid, df['x'], df['p'], p0=[-1, np.log(np.median(df['x']))])
            a, b = popt
            x_target = np.exp(-b/a)
            dls.append(x_target)
            p_fit = sigmoid(x_range, a, b)
            ps.append(p_fit)
            # plt
            ax.plot(df['x'], df['p'], 'o', color=color[0])
            ax.plot(x_range, p_fit, color=color[1])
            ax.axvline(x_target, color='orange', linestyle='--', label='$\Delta{T}_{DL}$ = '+f'{x_target:.1f}ms')
            ax.axhline(0.5, color='k', linestyle='--', label='$P(\Delta{T})=0.5$')
            ax.set_xscale('log')
            ax.set_xlim([10, 1000])
            ax.set_xlabel('ずれ $\Delta{T}$ [ms]')
            ax.set_ylabel('確率 $P(\Delta{T})$')
            ax.set_title(f'T={P}ms')
            ax.legend(loc='upper left', fontsize=8)
            ax.grid(True)
        fig.delaxes(axes.flat[-1])
        plt.tight_layout()
        plt.savefig(os.path.join(IMGDIR, f'summary_sigmoid_tone_ba_{sl}.png'))
        plt.show()


if __name__ == "__main__":
    main()