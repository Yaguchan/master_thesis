import os
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt


# python 3.3/plt_tone_ps.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def before_value(time, M=1):
    n1 = 0.0838
    a1 = 39.4
    n2 = 1.04
    a2 = 0.281
    T = 176
    abs_time = abs(time)
    if abs_time <= T:
        y = (abs_time)**(-n1+1) / ((-n1+1) * a1)
    else:
        y = T**(-n1+1) / ((-n1+1) * a1)
        y += ((abs_time)**(-n2+1) - T**(-n2+1)) / ((-n2+1) * a2)
    if time < 0: y *= -1
    return y * M


def after_value(time, M=1):
    n1 = 0.158
    a1 = 39.2
    n2 = 0.317
    a2 = 18.6
    T = 109
    abs_time = abs(time)
    if abs_time <= T:
        y = (abs_time)**(-n1+1) / ((-n1+1) * a1)
    else:
        y = T**(-n1+1) / ((-n1+1) * a1)
        y += ((abs_time)**(-n2+1) - T**(-n2+1)) / ((-n2+1) * a2)
    if time < 0: y *= -1
    return y * M


def main():
    M = 1000
    MIN = 0
    MAX = 1000
    base_m = 1000
    data_s = np.linspace(MIN, MAX, MAX-MIN+1)
    before_ps = []
    after_ps = []
    after_m = base_m / after_value(base_m)
    
    # 集計
    for s in data_s:
        before_ps.append(before_value(s, after_m))
        after_ps.append(after_value(s, after_m))
    
    # plt
    plt.figure(figsize=(6, 6))
    plt.plot(data_s, before_ps, 'b', label='$\it{T}-\Delta\it{T}$')
    plt.plot(data_s, after_ps, 'r', label='$\it{T}+\Delta\it{T}$')
    # plt.plot(data_s, all_ss, 'g', label='all')
    plt.plot(data_s, data_s, 'k', linestyle='--')
    plt.xlabel('物理時間 $\it{t}$ [ms]', fontsize=15)
    # plt.xlabel('Physical Time $\it{t}$ [ms]', fontsize=15)
    plt.ylabel(r'心理時間 $\tau$ [mps]', fontsize=15)
    # plt.ylabel(r'Psychological Time $\tau$ [mps]', fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    plt.legend(fontsize=10, title="間隔の長短", loc='upper left')
    # plt.legend(fontsize=10, title="Short・Long", loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'ps_tone.png'))
    plt.show()

if __name__ == '__main__':
    main()