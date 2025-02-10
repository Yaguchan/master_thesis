import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.linear_model import LinearRegression


# python 3.3/plt_tone_dl.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def main():
    
    # ms -> s
    M = 1000
    MIN = 10
    MAX = 1000
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    deltas = [  [47.613188138905365, 52.200283919138606, 56.75971346962946, 56.18937193764298, 69.44414352573199, 137.01290397671463, 292.5698375620828],
                [59.93659720739624, 63.43625231076085, 71.91237259702216, 82.85336153024254, 97.32043871773085, 130.44512076191359, 150.96713498986563]]
    x_range = np.linspace(MIN, MAX, MAX-MIN+1)
    x_data = np.array(Ps).reshape(-1, 1)
    plt.figure(figsize=(6, 6))
    
    for deltas_ in deltas:
        for delta, P in zip(deltas_, Ps):
            print(delta/P)
        print()
    
    
    # 間隔が短くなる方向
    y_data = np.array(deltas[0])
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
    plt.plot(x_data, y_data, 'o', color='c', linestyle='None')
    x1_range = np.linspace(MIN, int(intersection), int(intersection)-MIN+1).reshape(-1, 1)
    y1_log_range = model_before1.predict(np.log(x1_range))
    x2_range = np.linspace(int(intersection), MAX, MAX-int(intersection)+1).reshape(-1, 1)
    y2_log_range = model_before2.predict(np.log(x2_range))
    plt.plot(x1_range, np.exp(y1_log_range), 'b', label='$\it{T}-\Delta\it{T}$')
    plt.plot(x2_range, np.exp(y2_log_range), 'b')
    
    
    # 間隔が長くなる方向
    y_data = np.array(deltas[1])
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
    plt.plot(x_data, y_data, 'o', color='m', linestyle='None')
    x1_range = np.linspace(MIN, int(intersection), int(intersection)-MIN+1).reshape(-1, 1)
    y1_log_range = model_before1.predict(np.log(x1_range))
    x2_range = np.linspace(int(intersection), MAX, MAX-int(intersection)+1).reshape(-1, 1)
    y2_log_range = model_before2.predict(np.log(x2_range))
    plt.plot(x1_range, np.exp(y1_log_range), 'r', label='$\it{T}+\Delta\it{T}$')
    plt.plot(x2_range, np.exp(y2_log_range), 'r')
    
        
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)  
    plt.xlim(10, 1000)
    plt.ylim(40, 400)
    plt.xlabel("物理時間 $\it{t}$ [ms]", fontsize=15)
    plt.ylabel("弁別閾 $\Delta\it{T}_{\it{DL}}$ [ms]", fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    plt.legend(fontsize=10, title="間隔の長短", loc='upper left')
    plt.tight_layout()
    #plt.tick_params(labelsize=15)
    plt.savefig(os.path.join(IMGDIR, f'dl_linear_tone.png'))
    plt.show()


if __name__ == '__main__':
    main()