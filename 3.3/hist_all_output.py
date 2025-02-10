import os
import math
import pandas as pd
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt
from collections import Counter
from scipy.optimize import curve_fit


# python 3.3/hist_all_output.py
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
    wavlens = [1000, 1500, 2000]
    N = 9
    M = 1e10
    MIN = 10
    MAX = 300
    
    # output list
    output_dict = {}
    for P in Ps:
        output_dict[P] = []
    for name in names:
        namedir = os.path.join(OUTPUTDIR, name)
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                if delta == -1: delta = M
                if sl == 1: continue
                output_dict[P].append(delta)
    
    all_deltas = []
    for P, max_delta in zip(Ps, max_deltas):
        deltas = []
        for i in range(N): 
            deltas.append(max_delta/(math.sqrt(2)**i))
        all_deltas.append(sorted(deltas))
    
    for P, deltas in zip(Ps, all_deltas):
        count = Counter(output_dict[P])
        total_count = sum(count.values())
        
        # 確率
        cumulative_count = 0
        cumulative_counts = {}
        probs = {k: v / total_count for k, v in count.items()}
        for delta in deltas:
            if not delta in probs: 
                probs[delta] = 0
        single_probs = {k: probs[k] for k in sorted(probs.keys())}
        # 累積和
        for value in sorted(deltas):
            cumulative_count += count.get(value, 0)  # 値が存在しない場合は0を加算
            cumulative_counts[value] = cumulative_count
        cumulative_probs = {k: v / total_count for k, v in cumulative_counts.items()}
        
        # plt
        fig, axs = plt.subplots(3, 1, figsize=(6, 9))
        
        def sigmoid(x, a, b):
            return 1 / (1 + np.exp(-(a * np.log(x) + b)))
        data = {
            "x": deltas,
            "p": cumulative_probs.values()
        }
        
        df = pd.DataFrame(data)
        popt, pcov = curve_fit(sigmoid, df['x'], df['p'], p0=[-1, np.log(np.median(df['x']))])
        a, b = popt
        x_target = np.exp(-b/a)
        x_fit = np.linspace(MIN, MAX, MAX-MIN+1)
        y_fit = sigmoid(x_fit, *popt)
        
        # single_probs
        pos = np.arange(len(deltas))
        deltas_ = [round(delta, 1) for delta in deltas]
        axs[0].bar(pos, height=single_probs.values(), width=1.0, color='c', edgecolor='black')
        axs[0].set_xlabel('ずれ $\Delta{T}$', fontsize=15)
        axs[0].set_ylabel('確率', fontsize=15)
        axs[0].set_xticks(pos, deltas_)
        axs[0].set_ylim(0, 1)
        axs[0].tick_params(axis='both', labelsize=13)
        
        # cumulative_probs
        axs[1].bar(pos, height=cumulative_probs.values(), width=1.0, color='c', edgecolor='black')
        axs[1].set_xlabel('ずれ $\Delta{T}$', fontsize=15)
        axs[1].set_ylabel('累積確率 $\it{P(\Delta{T})}$', fontsize=15)
        axs[1].set_xticks(pos, deltas_)
        axs[1].set_ylim(0, 1)
        axs[1].tick_params(axis='both', labelsize=13)
        
        for delta, prob in zip(deltas, cumulative_probs.values()):
            axs[2].plot(delta, prob, marker='o', color='c')
        axs[2].plot(x_fit, y_fit, 'b')
        axs[2].axvline(x_target, color='orange', linestyle='--', label='$\Delta{T}$'+f'={x_target:.2f}')
        axs[2].axhline(0.5, color='k', linestyle='--', label='$\it{P(\Delta{T})}$=0.5')
        axs[2].set_xscale('log')
        axs[2].set_xlabel('ずれ $\Delta{T}$', fontsize=15)
        axs[2].set_ylabel('累積確率 $\it{P(\Delta{T})}$', fontsize=15)
        axs[2].set_xlim(10, 270)
        axs[2].set_ylim(0, 1)
        axs[2].tick_params(axis='both', labelsize=13)
        axs[2].legend()
        
        plt.tight_layout()
        # plt.savefig(os.path.join(IMGDIR, f'{P}.png'))
        plt.savefig(os.path.join(IMGDIR, f'cal_dl.png'))
        plt.show()
        exit()


if __name__ == "__main__":
    main()