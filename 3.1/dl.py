import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.lines import Line2D
from sklearn.linear_model import LinearRegression


# python 3.1/dl.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.1'

def mid_log(x, y):
    return np.exp((np.log(x)+np.log(y))/2)


def main():
    
    # ms -> s
    M = 1000
    Ts = [100, 200, 400, 800, 1600]
    
    # raw data T+delta:[normal, reverse]
    data = {}
    data[0] = {}
    data[1] = {}
    data[0][100] = {50:[3, 4], 59:[7, 2], 71:[14, 4], 84:[15, 4]}
    data[1][100] = {119: [6, 13], 141:[2, 11], 168:[0, 4], 200:[0, 1]}
    data[0][200] = {113:[1, 1], 130:[2, 0], 150:[2, 3], 173:[13, 6]}
    data[1][200] = {231:[7, 9], 266:[3, 5], 307:[0, 2], 354:[0, 0]}
    data[0][400] = {261:[1, 0], 291:[0, 2], 323:[4, 2], 360:[6, 5]}
    data[1][400] = {445:[10, 10], 495:[5, 3], 550:[2, 2], 612:[1, 0]}
    data[0][800] = {615:[0, 3], 657:[3, 6], 702:[1, 11], 749:[6, 9]}
    data[1][800] = {854:[11, 8], 912:[3, 7], 974:[5, 0], 1040:[1, 2]}
    data[0][1600] = {1231:[1, 2], 1314:[2, 4], 1403:[4, 3], 1498:[4, 16]}
    data[1][1600] = {1708:[11, 5], 1824:[6, 3], 1948:[5, 2], 2080:[1, 1]}
    
    dl_minus = {}
    dl_plus = {}
    
    for i in range(2):
        for T in Ts:
            data[i][T][T] = [15, 15]
            keys = []
            values = []
            for key, value in sorted(data[i][T].items()):
                prob = sum(value) / 60
                keys.append(key)
                values.append(prob)
                if i == 0 and prob > 0.25:
                    t_dl = np.exp((0.25 - values[-2]) * (np.log(keys[-1]) - np.log(keys[-2])) / (values[-1] - values[-2]) + np.log(keys[-2]))
                    dl_minus[mid_log(t_dl, T)] = T - t_dl
                    break
                if i == 1 and prob < 0.25:
                    t_dl = np.exp((0.25 - values[-2]) * (np.log(keys[-1]) - np.log(keys[-2])) / (values[-1] - values[-2]) + np.log(keys[-2]))
                    dl_plus[mid_log(T, t_dl)] = t_dl - T
                    break
    
    dl_combined = {**dl_minus, **dl_plus}
    dl_combined = {key: dl_combined[key] for key in sorted(dl_combined)}
    x_data = np.array(list(dl_combined.keys()))
    y_data = np.array(list(dl_combined.values()))
    
    # fitting
    def lod(x, A, B):
        return np.exp(A * np.log(x) + B)
        # return 10 ** (A * np.log10(x) + B)
    model = LinearRegression()
    model.fit(np.log(x_data[4:]).reshape(-1, 1), np.log(y_data[4:]).reshape(-1, 1))
    A_fit = model.coef_
    B_fit = model.intercept_
    C_fit = np.average(y_data[:4])
    print('fitting')
    print('A', A_fit[0])
    print('B', B_fit)
    print('C', C_fit)
    print('------------------------------------')
    
    # plot
    plt.figure(figsize=(6, 6))
    # point
    for i in range(len(x_data)): 
        if i % 2 == 0: color = 'c'
        else: color = 'm'
        plt.plot(x_data[i], y_data[i], 'o', color=color) 
    
    # const
    plt.plot([0, 310], [C_fit, C_fit], 'r')
    
    # line
    x_range = np.linspace(310, 2000, 1000)
    x_s_range = x_range
    y_s_range = lod(x_range, A_fit, B_fit)
    plt.plot(x_s_range, y_s_range.reshape(-1), 'r')
    
    
    # dl z
    dl_z = [30.498747491084664, 33.5328836032993, 53.49648869713307, 85.30547230701862, 160.1816353757621]
    plt.plot(Ts, dl_z, marker='x', color='gray', linestyle='None')
    
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)  
    plt.xlim(10, 2000)
    plt.xlabel('基準値 $\it{T}$ [ms]', fontsize=15)
    plt.ylabel('弁別閾 $\Delta\it{T}_{DL}$ [ms]', fontsize=15)
    
    # legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='c', label=r'error rate $\it{T}\times{\alpha} < \it{T}$'),
        Line2D([0], [0], marker='o', color='m', label=r'error rate $\it{T}\times{\alpha} > \it{T}$'),
        Line2D([0], [0], marker='x', color='gray', label='z score')
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    
    plt.tick_params(axis='both', labelsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'dl_error.png'))
    plt.show()

if __name__ == '__main__':
    main()