import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy.stats import norm
from sklearn.linear_model import LinearRegression


# python 3.1/summary_z_ba.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.1'


def mid_log(x, y):
    return np.exp((np.log(x)+np.log(y))/2)


def main():
    
    # ms -> s
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
    
    data2 = {}
    for T in Ts:
        data2[T] = {}
        for i in range(2):
            for key, value in data[i][T].items():
                if i == 0: prob = sum(value) / 60
                else: prob = (60 - sum(value)) / 60
                data2[T][key] = prob
    
    # sd/dlの算出
    dls = []
    # 標準正規分布の逆累積分布値を計算
    x_075 = norm.ppf(0.75)  # 0.75 の位置
    x_025 = norm.ppf(0.25)  # 0.25 の位置
    print(x_075, x_025)
    half_range = (x_075 - x_025) / 2
    fig, axes = plt.subplots(3, 2, figsize=(8, 12))
    for T, ax in zip(Ts, axes.flat):
        data = {
            "x": data2[T].keys(),
            "p": data2[T].values()
        }
        df = pd.DataFrame(data)
        df = df[df["p"]!=0]
        df = df[df["p"]!=1]
        df["z"] = norm.ppf(df["p"])
        X = np.array(df["x"]).reshape(-1, 1)
        y = df["z"]
        model = LinearRegression().fit(X, y)
        slope = model.coef_[0]
        intercept = model.intercept_
        sd = 1 / slope
        dl = half_range * sd
        dls.append(dl)
        # plt
        ax.plot(df["x"], df["z"], marker='o', linestyle='None')
        # linear
        x = np.linspace(min(df["x"]), max(df["x"]))
        z = slope * x + intercept
        ax.plot(x, z, color='r')
        ax.set_xlabel(r'間隔 $T\times\alpha$ [ms]')
        ax.set_ylabel('z-score')
        ax.set_title(f'T={T}ms')
    fig.delaxes(axes.flat[-1])
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'linear_z.png'))
    plt.show()



if __name__ == '__main__':
    main()