import os
import math
import japanize_matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scipy.optimize import curve_fit


# python 3.3/histgram_ba.py
OUTPUTDIR = '/Users/user/Desktop/授業/lab/資料/知覚実験3/output_v3'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3/histgram'


def main():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # output data
    names = os.listdir(OUTPUTDIR)
    names = [name for name in names if name != '.DS_Store']
    
    # test
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    # max_deltas = [200, 200, 200, 200, 200, 400, 800]
    max_deltas = [400, 400, 400, 400, 400, 400, 800]
    N = 9
    M = 1e10
    MIN = 1
    MAX = 1000
    
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
                # if delta == -1: continue
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
        for P, deltas in zip(Ps, all_deltas):
            plt.figure(figsize=(8, 6))
            # 確率
            count = Counter(output_dict[P])
            total_count = sum(count.values())
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
            pos = np.arange(len(deltas))
            deltas_ = [round(delta, 1) for delta in deltas]
            plt.bar(pos, height=cumulative_probs.values(), width=1.0, color='c', edgecolor='black')
            plt.xlabel('ずれ $\Delta{T}$', fontsize=15)
            plt.ylabel('累積確率 $\it{P(\Delta{T})}$', fontsize=15)
            plt.xticks(pos, deltas_)
            plt.ylim(0, 1)
            plt.tight_layout()
            plt.savefig(os.path.join(IMGDIR, f'histgram_cprob_ba_{sl}_{P}.png'))
            plt.show()


if __name__ == "__main__":
    main()