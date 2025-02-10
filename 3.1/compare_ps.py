import os
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt


# python 3.1/compare_ps.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.1'


def before_value(time, M=118.53855840405375):
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


def after_value(time, M=118.53855840405375):
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


def asj2023_value(time, M=47.298210101417965):
    alpha = 0.8
    K = np.exp(-1.06)
    T = 310
    y = 0
    abs_time = abs(time)
    if 0 <= abs_time <= T:
        y += abs_time / 33.9
    else:
        y += T / 33.9
        y += (abs_time**(-alpha+1) - T**(-alpha+1)) / ((-alpha+1) * K)
    if time < 0: y *= -1
    return y * M


def main():
    M = 1000
    MIN = 0
    MAX = 1000
    data_s = np.linspace(MIN, MAX, MAX-MIN+1)
    before_ps = []
    after_ps = []
    asj2023_ps = []
    # after_m = base_m / after_value(base_m)
    # print(after_m)
    
    # 集計
    for s in data_s:
        before_ps.append(before_value(s))
        after_ps.append(after_value(s))
        asj2023_ps.append(asj2023_value(s))
        
    print(before_value(600)-before_value(400))
    print(after_value(800)-after_value(600))
    
    # plt
    plt.figure(figsize=(6, 6))
    plt.plot(data_s, before_ps, 'b', label='$\it{T}-\Delta\it{T}$')
    plt.plot(data_s, after_ps, 'r', label='$\it{T}+\Delta\it{T}$')
    plt.plot(data_s, asj2023_ps, 'gray')
    # plt.plot(data_s, all_ss, 'g', label='all')
    # plt.plot(data_s, data_s, 'k', linestyle='--')
    plt.xlabel('物理時間 $\it{t}$ [ms]', fontsize=15)
    # plt.xlabel('Physical Time $\it{t}$ [ms]', fontsize=15)
    plt.ylabel(r'心理時間 $\tau$ [mps]', fontsize=15)
    # plt.ylabel(r'Psychological Time $\tau$ [mps]', fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    plt.legend(fontsize=10, title="間隔の長短", loc='upper left')
    # plt.legend(fontsize=10, title="Short・Long", loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'ps_curves.png'))
    plt.show()

if __name__ == '__main__':
    main()