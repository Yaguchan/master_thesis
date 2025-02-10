import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.linear_model import LinearRegression


# python 3.3/plt_dl_wavlen.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def main():
    
    # ms -> s
    M = 1000
    MIN = 10
    MAX = 1000
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    wavlens = [1000, 1500, 2000]
    before_deltas = [   [44.190644195319315, 42.133228427872076, 49.71979826703801, 53.78584599488387, 69.07161225054475, 104.97903401490792, 255.6789492187238],
                        [43.715526191493325, 50.735330844563265, 56.971946612303135, 58.581395633148425, 66.3906794718752, 156.855186651121, 278.5759867156664],
                        [58.666877871767774, 66.29522843441457, 64.42416095405143, 56.34229464586939, 71.55018109200451, 150.4541241468546, 347.83560572599686]]
    after_deltas = [    [56.40498897316301, 61.65564953872158, 66.98337637372933, 74.09739279049822, 82.0822608456563, 126.65088957468852, 120.39721968885613],
                        [62.899241191058714, 61.511341394841686, 72.42190421766529, 83.70434228915842, 96.54013789522813, 115.80504939401547, 161.00911706841126],
                        [60.59646243548518, 67.51009579331655, 77.49812528664981, 87.27988724588143, 110.02520688470003, 155.45541955935073, 174.86210478826501]]
    x_range = np.linspace(MIN, MAX, MAX-MIN+1)
    x_data = np.array(Ps).reshape(-1, 1)
    plt.figure(figsize=(6, 6))
    
    # 前
    colors = ['lightblue', 'blue', 'darkblue']
    for deltas, wavlen, color in zip(before_deltas, wavlens, colors):
        y_data = np.array(deltas)
        model_before1 = LinearRegression()
        model_before1.fit(np.log(x_data[:4]), np.log(y_data[:4]))
        A1_fit = model_before1.coef_
        B1_fit = model_before1.intercept_
        a1_fit = np.exp(B1_fit)
        n1_fit = A1_fit
        model_before2 = LinearRegression()
        model_before2.fit(np.log(x_data[4:]), np.log(y_data[4:]))
        A2_fit = model_before2.coef_
        B2_fit = model_before2.intercept_
        a2_fit = np.exp(B2_fit)
        n2_fit = A2_fit
        intersection = np.exp(np.log(a1_fit/a2_fit)/(n2_fit-n1_fit)).item()
        print('fitting before')
        print(f'〜100ms   A:{A1_fit[0]}, B:{B1_fit}')
        print(f'〜100ms   n:{A1_fit[0]}, a:{np.exp(B1_fit)}')
        print(f'200〜ms   A:{A2_fit[0]}, B:{B2_fit}')
        print(f'200〜ms  n:{A2_fit[0]}, a:{np.exp(B2_fit)}')
        print('交点', intersection)
        plt.plot(x_data, y_data, 'o', color=color, linestyle='None')
        x1_range = np.linspace(MIN, int(intersection), int(intersection)-MIN+1).reshape(-1, 1)
        y1_log_range = model_before1.predict(np.log(x1_range))
        x2_range = np.linspace(int(intersection), MAX, MAX-int(intersection)+1).reshape(-1, 1)
        y2_log_range = model_before2.predict(np.log(x2_range))
        plt.plot(x1_range, np.exp(y1_log_range), color=color, label='$\it{T}-\Delta\it{T}$ '+f'D={wavlen}ms')
        plt.plot(x2_range, np.exp(y2_log_range), color=color)
    
    # 後
    colors = ['lightsalmon', 'red', 'darkred']
    for deltas, wavlen, color in zip(after_deltas, wavlens, colors):
        y_data = np.array(deltas)
        model_after = LinearRegression()
        model_after.fit(np.log(x_data), np.log(y_data))
        A_fit = model_after.coef_
        B_fit = model_after.intercept_
        print('fitting before')
        print(f'A:{A_fit[0]}, B:{B_fit}')
        print(f'n:{A_fit[0]}, a:{np.exp(B_fit)}')
        x_range = np.linspace(MIN, MAX, MAX-MIN+1).reshape(-1, 1)
        print(np.exp(A_fit*np.log(100)+B_fit))
        x_log_range = np.log(x_range)
        y_log_range = model_after.predict(x_log_range)
        plt.plot(x_data, y_data, 'o', color=color, linestyle='None')
        plt.plot(x_range, np.exp(y_log_range), color=color, label='$\it{T}+\Delta\it{T}$ '+f'D={wavlen}ms')
    
        
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)  
    plt.xlim(10, 1000)
    plt.ylim(10, 400)
    plt.xlabel("物理時間 $\it{t}$ [ms]", fontsize=15)
    plt.ylabel("弁別閾 $\Delta\it{T}_{\it{DL}}$ [ms]", fontsize=15)
    plt.tick_params(axis='both', labelsize=15)
    plt.legend(fontsize=10)
    plt.tight_layout()
    #plt.tick_params(labelsize=15)
    plt.savefig(os.path.join(IMGDIR, f'dl_linear_tone.png'))
    plt.show()


if __name__ == '__main__':
    main()