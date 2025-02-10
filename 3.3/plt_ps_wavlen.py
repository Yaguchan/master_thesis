import os
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt


# python plt_ps_wavlen.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img'


def two_linear(time, M, n1, a1, n2, a2, T):
    abs_time = abs(time)
    if abs_time <= T:
        y = (abs_time)**(-n1+1) / ((-n1+1) * a1)
    else:
        y = T**(-n1+1) / ((-n1+1) * a1)
        y += ((abs_time)**(-n2+1) - T**(-n2+1)) / ((-n2+1) * a2)
    if time < 0: y *= -1
    return y * M


def one_linear(time, M, n, a):
    abs_time = abs(time)
    y = abs_time**(-n+1) / ((-n+1) * a)
    if time < 0: y *= -1
    return y * M

def main():
    M = 1000
    MIN = 0
    MAX = 1000
    base_m = 1000
    M = base_m / one_linear(base_m, 1, 0.2326716490018949, 30.401394912905882)
    data_s = np.linspace(MIN, MAX, MAX-MIN+1)
    
    # labels
    before_labels = [
        '$\it{T}-\Delta\it{T}$ D=1000ms',
        '$\it{T}-\Delta\it{T}$ D=1500ms',
        '$\it{T}-\Delta\it{T}$ D=2000ms',
        '$\it{T}-\Delta\it{T}$',
    ]
    after_labels = [
        '$\it{T}+\Delta\it{T}$ D=1000ms',
        '$\it{T}+\Delta\it{T}$ D=1500ms',
        '$\it{T}+\Delta\it{T}$ D=2000ms',
        '$\it{T}+\Delta\it{T}$',
    ]
    
    # params
    before_params = [
        [0.10893188018917553, 32.03406060251564, 0.944084290051377, 0.42934039665053986, 174.77415151839776],
        [0.14341513453250035, 31.280224534791667, 1.0345091402874371, 0.28995351660746493, 191.16112158511996],
        [-0.021628688036957684, 66.21108240066876, 1.1406891481247294, 0.16710445505365346, 171.84608038079375],
        [0.08376177750774247, 39.36155808719251, 1.0374280529756565, 0.2810339917635561, 178.07039669]
    ]
    after_params = [
        [0.2018604994109664, 31.711185832374547],
        [0.22529764305771566, 31.326028888647215],
        [0.26782102955344134, 28.3541900115481],
        [0.2326716490018949, 30.401394912905882]
    ]
    
    # colors
    before_colors = ['lightblue', 'blue', 'darkblue', 'blue']
    after_colors = ['lightsalmon', 'red', 'darkred', 'red']
    
    # plt
    plt.figure(figsize=(6, 6))
    for i, (param, label, color) in enumerate(zip(before_params, before_labels, before_colors)):
        ss = []
        for s in data_s:
            ss.append(two_linear(s, M, *param))
        if i == 3: linestyle = '-'
        else: linestyle = '--'
        plt.plot(data_s, ss, label=label, linestyle=linestyle, color=color)
    for i, (param, label, color) in enumerate(zip(after_params, after_labels, after_colors)):
        ss = []
        for s in data_s:
            ss.append(one_linear(s, M, *param))
        if i == 3: linestyle = '-'
        else: linestyle = '--'
        plt.plot(data_s, ss, label=label, linestyle=linestyle, color=color)
    plt.xlabel('物理時間 $\it{T}$ [ms]', fontsize=15)
    plt.ylabel(r'心理時間 $\tau$ [mps]', fontsize=15)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'ps_wavlen.png'))
    plt.show()

if __name__ == '__main__':
    main()