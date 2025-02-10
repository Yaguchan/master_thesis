import os
import math
import japanize_matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scipy.optimize import curve_fit


# python 3.3/dl_all_pause.py
OUTPUT1DIR = '/Users/user/Desktop/授業/lab/資料/知覚実験2/output_v2'
OUTPUT2DIR = '/Users/user/Desktop/授業/lab/資料/知覚実験3/output_v3'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def tone():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # test
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    
    list_max_deltas = [[200, 200, 200, 200, 200, 400, 800], [400, 400, 400, 400, 400, 400, 800]]
    wavlens = [1000, 1500]
    outdirs = [OUTPUT1DIR, OUTPUT2DIR]
    N = 9
    NA = 1e10
    
    # 音声だけ + pause
    # -20dB, 6/6/233/303
    # -30dB, 2/2/186/207
    # -40dB, 0/0/167/186
    # -50dB, 0/0/48/77
    list_pauses = [[0, 0], [167, 186]]
    list_pause_Ps = {}
    for i in range(2):
        list_pause_Ps[i] = {}
        for wavlen in wavlens:
            list_pause_Ps[i][wavlen] = []
    for i, pauses in enumerate(list_pauses):
        for wavlen, pause in zip(wavlens, pauses):
            for P in Ps:
                list_pause_Ps[i][wavlen].append(P+pause)
    print(list_pause_Ps)
    
    # output list
    output1_before_dict = {}
    output1_after_dict = {}
    output2_before_dict = {}
    output2_after_dict = {}
    for wavlen in wavlens:
        output1_before_dict[wavlen] = {}
        output1_after_dict[wavlen] = {}
        output2_before_dict[wavlen] = {}
        output2_after_dict[wavlen] = {}
        for P in Ps:
            output1_before_dict[wavlen][P] = []
            output1_after_dict[wavlen][P] = []
            output2_before_dict[wavlen][P] = []
            output2_after_dict[wavlen][P] = []
    for i, outdir in enumerate(outdirs):
        names = os.listdir(outdir)
        names = [name for name in names if name != '.DS_Store']
        for name in names:
            namedir = os.path.join(outdir, name)
            with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
                for line in file:
                    sl, wavlen, P, delta = line.split(' ')
                    sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                    if wavlen == 2000: continue
                    if delta == -1: delta = NA
                    if i == 0:
                        if sl == 0: output1_before_dict[wavlen][P].append(delta)
                        else: output1_after_dict[wavlen][P].append(delta)
                    else:
                        if sl == 0: output2_before_dict[wavlen][P].append(delta)
                        else: output2_after_dict[wavlen][P].append(delta)
    
    # cal dl
    def sigmoid(x, a, b):
        return 1 / (1 + np.exp(-(a * np.log(x) + b)))
    list_colors = [['lightblue', 'blue'], ['lightsalmon', 'red']]
    signal_labels = ['純音', '音声']
    sl_labels = ['$\it{T}-\Delta\it{T}$', '$\it{T}+\Delta\it{T}$']
    # list_colors = [['lightblue', 'blue'], ['lightblue', 'blue']]
    # list_colors = [['r', 'b'], ['r', 'b']]
    plt.figure(figsize=(6, 6))
    for i, (pause_Ps, max_deltas, signal_label) in enumerate(zip(list_pause_Ps, list_max_deltas, signal_labels)):
        if i == 0: 
            linestyle = '--'
            marker = 'x'
        else: 
            linestyle = '-'
            marker = 'o'
        all_deltas = []
        for P, max_delta in zip(Ps, max_deltas):
            deltas = []
            for j in range(N):
                deltas.append(max_delta/(math.sqrt(2)**j))
            all_deltas.append(sorted(deltas))
        for sl, (sl_label, colors) in enumerate(zip(sl_labels, list_colors)):
            # if sl == 0: 
            #     # linestyle = '-'
            #     marker = 'o'
            # else: 
            #     # linestyle = '--'
            #     marker = 'o'
            for wavlen, color in zip(wavlens, colors):
                if i == 0:
                    if sl == 0: output_dict = output1_before_dict[wavlen]
                    else: output_dict = output1_after_dict[wavlen]
                else:
                    if sl == 0: output_dict = output2_before_dict[wavlen]
                    else: output_dict = output2_after_dict[wavlen]
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
                    # print(x_target)
                    dls.append(x_target)
                # print(sl, wavlen, np.average(dls))
                print(dls)
                if sl == 0:
                    if wavlen == 1000: color = '#9999FF'
                    else: color = '#3333FF'
                else:
                    if wavlen == 1000: color = '#FF9999'
                    else: color = '#FF3333'
                plt.plot(list_pause_Ps[i][wavlen], dls, marker=marker, color=color, linestyle=linestyle, label=f'{signal_label}/{sl_label}/{wavlen}ms')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlim(10, 1100)
    plt.ylim(40, 300)
    plt.xlabel('基準値 $\it{T}_{-40dBFS}$', fontsize=15)
    plt.ylabel('弁別閾 $\Delta\it{T}_{DL}$', fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    plt.legend(fontsize=10, title="信号$\it{S}$/間隔の長短/信号長$\it{D}$")
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'dl_all_pause.png'))
    plt.show()


if __name__ == "__main__":
    tone()