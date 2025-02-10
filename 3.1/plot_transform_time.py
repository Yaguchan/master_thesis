import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt

# python 3.1/plot_transform_time.py

def cal_value(time):
    M = 3.1 #33.9
    alpha = 0.8
    K = np.exp(-1.06)
    T = 310
    y = 0
    if time <= -T:
        y -= T / M
        y -= ((-time)**(-alpha+1) - T**(-alpha+1)) / ((-alpha+1) * K)
    elif -T <= time <= 0:
        # -310 <= time <= 0
        y += time / M
    elif 0 <= time <= T:
        # 0 <= time <= 310
        y += time / M
    elif time >= T:
        # 0 <= time <= 310
        y += T / M
        # 310 <= time
        y += (time**(-alpha+1) - T**(-alpha+1)) / ((-alpha+1) * K)
    return y * M


def cal_value2(time, M=47.298210101417965):
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

    # 関数 [200, 1600]
    # x_data = np.linspace(-2000, 2000, 1000)
    x_data = np.linspace(-2, 2, 1000)
    # x_data = np.linspace(0, 2000, 1000)
    y_data = []
    for x in x_data:
        # y_data.append(cal_value(x))
        # y_data.append(cal_value(x * 1000))
        y_data.append(cal_value2(x * 1000))
    y_data = np.array(y_data)
    plt.plot(x_data, y_data, 'r', label='Fitted Curve')
    
    
    
    # [ms] 表記
    # plt.plot([-2000, 2000], [0, 0], 'k', linewidth=1, label='Fitted Curve')
    # plt.plot([0, 0], [-1500, 1500], 'k', linewidth=1, label='Fitted Curve')
    # plt.xlim(-2000, 2000)
    # plt.ylim(-1500, 1500)
    # plt.xlabel('物理時間 t [ms]', fontsize=25)
    # plt.xlabel('Physical Time t [ms]', fontsize=25)
    # plt.ylabel('感覚時間 τ [mss]', fontsize=25)
    # plt.ylabel('Sensation Time τ [mss]', fontsize=25)
    
    # [s] 表記
    # plt.plot([-2, 2], [0, 0], 'k', linewidth=1, label='Fitted Curve')
    # plt.plot([0, 0], [-1.25, 1.25], 'k', linewidth=1, label='Fitted Curve')
    # plt.xlim(-2, 2)
    # plt.ylim(-1.25, 1.25)
    # plt.xlim(0, 2)
    # plt.ylim(0, 1.25)
    # plt.xlabel(r'物理時間 $\it{t}$ [s]', fontsize=25)
    # plt.xlabel(r'Physical Time $\it{t}$ [s]', fontsize=25)
    # plt.ylabel(r'感覚時間 $\tau$ [ss]', fontsize=25)
    # plt.ylabel(r'Sensation Time $\tau$ [ss]', fontsize=25)
    
    plt.tick_params(labelsize=20)

    plt.show()

if __name__ == '__main__':
    main()