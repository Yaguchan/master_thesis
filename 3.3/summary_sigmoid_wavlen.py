import os
import math
import japanize_matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from collections import Counter
from scipy.optimize import curve_fit


# python 3.3/summary_sigmoid_wavlen.py
OUTPUTDIR = '/Users/user/Desktop/授業/lab/資料/知覚実験3/output_v3'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def main():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # output data
    names = os.listdir(OUTPUTDIR)
    names = [name for name in names if name != '.DS_Store']
    
    # tone/speech
    # max_deltas = [200, 200, 200, 200, 200, 400, 800]
    # wavlens = [1000, 1500, 2000]
    max_deltas = [400, 400, 400, 400, 400, 400, 800]
    wavlens = [1000, 1500]
    
    # 
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    list_colors = [['#9999FF', '#3333FF', '#000099'], ['#FF9999', '#FF3333', '#990000']]
    N = 9
    M = 1e10
    MIN = 1
    MAX = 1000
    
    # linear/log
    x_range = np.linspace(MIN, MAX, (MAX-MIN)*1+1)
    
    # output list
    output_before_dict = {}
    output_after_dict = {}
    for wavlen in wavlens:
        output_before_dict[wavlen] = {}
        output_after_dict[wavlen] = {}
        for P in Ps:
            output_before_dict[wavlen][P] = []
            output_after_dict[wavlen][P] = []
    
    for name in names:
        namedir = os.path.join(OUTPUTDIR, name)
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                if delta == -1: delta = M
                if sl == 0:
                    output_before_dict[wavlen][P].append(delta)
                else:
                    output_after_dict[wavlen][P].append(delta)
    
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
    for sl, (output_dict, colors) in enumerate(zip(output_dicts, list_colors)):
        raw_ps = []
        ps = []
        dls = []
        fig, axes = plt.subplots(4, 2, figsize=(8, 12))
        for P, deltas, ax in zip(Ps, all_deltas, axes.flat):
            for wavlen, color in zip(wavlens, colors):
                # 確率
                count = Counter(output_dict[wavlen][P])
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
                ax.plot(df['x'], df['p'], 'o', color=color)
                ax.plot(x_range, p_fit, color=color)
                ax.axvline(x_target, color=color, linestyle='--', label='$\Delta{T}_{DL}$ = '+f'{x_target:.1f}ms')
                # ax.axhline(0.5, color='k', linestyle='--', label='$P(\Delta{T})=0.5$')
                ax.set_xscale('log')
                ax.set_xlim([10, 1000])
                ax.set_xlabel('ずれ $\Delta{T}$ [ms]')
                ax.set_ylabel('確率 $P(\Delta{T})$')
                ax.set_title(f'T={P}ms')
                ax.legend(loc='upper left', fontsize=8)
                ax.grid(True)
        # fig.delaxes(axes.flat[-1]) 
        # 凡例作成
        axes.flat[-1].axis('off')
        lines = [
            mlines.Line2D([], [], color=color, linestyle='--', linewidth=2, label=f'D={wavlen}ms')
            for color, wavlen in zip(colors, wavlens)
        ]
        axes.flat[-1].legend(handles=lines, loc='center', fontsize=15)
        plt.tight_layout()
        plt.savefig(os.path.join(IMGDIR, f'summary_sigmoid_speech_wavlen_{sl}.png'))
        plt.show()


if __name__ == "__main__":
    main()