import os
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt


# python 4/example_ps.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/4'


# 評価
def psychological_differences(true, pred, M=1):
    if pred <= true: return before_value(true, M) - before_value(pred, M)
    else: return after_value(pred, M) - after_value(true, M)


def before_value(time, M=1):
    n1 = 0.0709
    a1 = 70.9
    n2 = 0.534
    a2 = 7.26
    T = 137
    abs_time = abs(time)
    if abs_time <= T:
        y = (abs_time)**(-n1+1) / ((-n1+1) * a1)
    else:
        y = T**(-n1+1) / ((-n1+1) * a1)
        y += ((abs_time)**(-n2+1) - T**(-n2+1)) / ((-n2+1) * a2)
    if time < 0: y *= -1
    return y * M

def after_value(time, M=1):
    n1 = 0.0245
    a1 = 73.9
    n2 = 0.396
    a2 = 11.1
    T = 165
    abs_time = abs(time)
    if abs_time <= T:
        y = (abs_time)**(-n1+1) / ((-n1+1) * a1)
    else:
        y = T**(-n1+1) / ((-n1+1) * a1)
        y += ((abs_time)**(-n2+1) - T**(-n2+1)) / ((-n2+1) * a2)
    if time < 0: y *= -1
    return y * M


def main():
    
    base_m = 1000
    m = base_m / after_value(base_m)
    
    # cal ps
    deltas = [300, 600]
    list_ps = []
    list_s = []
    for delta in deltas:
        ps = []
        for i, timing in enumerate(range(0, 1000, 100)):
            ps.append(psychological_differences(timing, timing+delta, m))
        list_ps.append(ps)
        list_s.extend([delta for _ in range(i+1)])
    
    # plt
    plt.figure(figsize=(6, 4))
    
    # hist
    all_list_ps = [item for sublist in list_ps for item in sublist]
    MIN = (min(all_list_ps) // 50) * 50
    MAX = (max(all_list_ps) // 50) * 50
    width = 50
    bins = np.arange(MIN, MAX+width, width)
    
    # 物理
    hist1, _ = np.histogram(list_s, bins=bins)
    bar_width = 0.4
    x = np.arange(len(hist1))
    plt.bar(x - bar_width / 2, hist1, width=bar_width, label='s', color='gray', edgecolor='k')
    
    # 心理
    colors = ['b', 'c']
    bottom = np.zeros(len(x))
    for ps, delta, color in zip(list_ps, deltas, colors):
        print(ps)
        hist, _ = np.histogram(ps, bins=bins)
        plt.bar(x + bar_width / 2, hist, width=bar_width, label=f'ps', color=color, edgecolor='k', bottom=bottom)
        bottom += hist
    labels = [f'{int(bins[i])}〜' for i in x]
    plt.xticks(x, labels, fontsize=11)
    plt.xlabel(r'物理/心理時間差 $\it{t}$[ms]/$\tau$[mps]', fontsize=15)
    plt.ylabel('頻度', fontsize=15)
    # plt.tick_params(axis='both', labelsize=13)
    plt.tight_layout()
    plt.legend(fontsize=12, loc='upper left')
    plt.savefig(os.path.join(IMGDIR, f'example_ps.png'))
    plt.show()


def main2():
    
    base_m = 1000
    m = base_m / after_value(base_m)
    
    # cal ps
    deltas = [500, 1000]
    list_before_ps = []
    list_after_ps = []
    list_s = []
    for delta in deltas:
        before_ps = []
        after_ps = []
        for i, timing in enumerate(range(0, 1500, 100)):
            before_ps.append(psychological_differences(timing+delta, timing, m))
            after_ps.append(psychological_differences(timing, timing+delta, m))
        list_before_ps.append(before_ps)
        list_after_ps.append(after_ps)
        list_s.extend([delta for _ in range(i+1)])
    
    # plt
    plt.figure(figsize=(6, 4))
    
    # hist
    all_list_ps = [item for sublist in list_before_ps + list_after_ps for item in sublist]
    MIN = (min(all_list_ps) // 50) * 50
    MAX = (max(all_list_ps) // 50) * 50
    width = 50
    bins = np.arange(MIN, MAX+width, width)
    
    # 物理
    hist1, _ = np.histogram(list_s, bins=bins)
    x = np.arange(len(hist1))
    plt.bar(x, hist1, width=1.0, label='s', color='gray', edgecolor='k')
    
    # 心理
    labels = ['$\it{T}-\Delta\it{T}$', '$\it{T}+\Delta\it{T}$']
    list_colors = [['c', 'b'], ['m', 'r']]
    bottom = np.zeros(len(x))
    for list_ps, colors, label in zip([list_before_ps, list_after_ps], list_colors, labels):
        for ps, delta, color in zip(list_ps, deltas, colors):
            print(ps)
            hist, _ = np.histogram(ps, bins=bins)
            plt.bar(x, hist, width=1.0, color=color, edgecolor='k', label=f'{label} {delta}ms', bottom=bottom)
            bottom += hist
    labels = [f'{int(bins[i])}〜' for i in x]
    plt.xticks(x, labels, fontsize=11)
    plt.xlabel(r'物理/心理時間差 $\it{t}$[ms]/$\tau$[mps]', fontsize=15)
    plt.ylabel('頻度', fontsize=15)
    # plt.tick_params(axis='both', labelsize=13)
    plt.tight_layout()
    plt.legend(fontsize=12, loc='upper left')
    plt.savefig(os.path.join(IMGDIR, f'example_ps.png'))
    plt.show()
    

def main3():
    
    base_m = 1000
    m = base_m / after_value(base_m)
    
    # cal ps
    deltas = [250, 500]
    list_before_ps = {}
    list_after_ps = {}
    list_s = {}
    for delta in deltas:
        list_before_ps[delta] = []
        list_after_ps[delta] = []
        for i, timing in enumerate(range(0, 1000, 100)):
            if delta == deltas[1]:
                list_before_ps[delta].append(psychological_differences(timing+delta, timing, m))
            list_after_ps[delta].append(psychological_differences(timing, timing+delta, m))
        list_s[delta] = [delta for _ in range(i+1)]
    
    # plt
    fig, axes = plt.subplots(2, 1, figsize=(6, 6))
    bar_width = 0.45
    YMAX = 8
    
    # hist
    all_list_ps = [v for d in (list_before_ps, list_after_ps) for lst in d.values() for v in lst]
    MIN = (min(all_list_ps) // 100) * 100
    MAX = (max(all_list_ps) // 100 + 1) * 100
    width = 100
    bins = np.arange(MIN, MAX+width, width)
    
    # histgram
    hist_s0, _ = np.histogram(list_s[deltas[0]], bins=bins)
    hist_s1, _ = np.histogram(list_s[deltas[1]], bins=bins)
    hist_before_ps0, _ = np.histogram(list_before_ps[deltas[0]], bins=bins)
    hist_before_ps1, _ = np.histogram(list_before_ps[deltas[1]], bins=bins)
    hist_after_ps0, _ = np.histogram(list_after_ps[deltas[0]], bins=bins)
    hist_after_ps1, _ = np.histogram(list_after_ps[deltas[1]], bins=bins)
    x = np.arange(len(hist_s0))
    
    # phy
    # bottom = np.zeros(len(x))
    # axes[0].bar(x, hist_s1, width=1.0, label='s', color='gray', edgecolor='k')
    # axes[1].bar(x, hist_s0, width=1.0, label='s', color='gray', edgecolor='k')
    # axes[1].bar(x, hist_s1, width=1.0, color='gray', edgecolor='k', bottom=bottom)
    
    # axes[0]
    axes[0].bar(x - bar_width / 2, hist_before_ps1, width=bar_width, color='b', edgecolor='k', label='$\it{T}-\Delta\it{T}$'+f' / {deltas[1]}ms')
    axes[0].bar(x + bar_width / 2, hist_after_ps1, width=bar_width, color='r', edgecolor='k', label='$\it{T}+\Delta\it{T}$'+f' / {deltas[1]}ms')
    labels = [f'{int(bins[i])}〜{int(bins[i+1])}' for i in x]
    axes[0].set_xticks(x, labels, fontsize=11)
    axes[0].set_ylim(0, YMAX)
    # axes[0].set_xlabel(r'物理/心理時間差 $\it{t}$[ms]/$\tau$[mps]', fontsize=15)
    axes[0].set_ylabel('頻度', fontsize=15)
    axes[0].legend(fontsize=10, loc='upper right', title='間隔の短長 / 物理時間差')
    
    # axes[1]
    axes[1].bar(x - bar_width / 2, hist_after_ps0, width=bar_width, color='#FF9999', edgecolor='k', label='$\it{T}+\Delta\it{T}$'+f' / {deltas[0]}ms')
    axes[1].bar(x + bar_width / 2, hist_after_ps1, width=bar_width, color='r', edgecolor='k', label='$\it{T}+\Delta\it{T}$'+f' / {deltas[1]}ms')
    labels = [f'{int(bins[i])}〜{int(bins[i+1])}' for i in x]
    axes[1].set_xticks(x, labels, fontsize=11)
    axes[1].set_xlabel(r'心理時間差 $|\tau_{true}-\tau_{pred}|$[mps]', fontsize=15)
    axes[1].set_ylabel('頻度', fontsize=15)
    axes[1].set_ylim(0, YMAX)
    axes[1].legend(fontsize=10, loc='upper right', title='間隔の短長 / 物理時間差')
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'example_ps.png'))
    plt.show()


if __name__ == '__main__':
    main3()