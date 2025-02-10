import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.linear_model import LinearRegression


# python 3.3/dl_linear_frame1.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def main():
    
    # ms -> s
    M = 1000
    MIN = 10
    MAX = 1000
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    deltas = [80.94077202274018, 86.73003977303192, 85.85082756421409, 90.35478934782152, 112.7784361649854, 127.18285026458156, 213.499988665226]
    x_range = np.linspace(MIN, MAX, MAX-MIN+1)
    x_data = np.array(Ps).reshape(-1, 1)
    plt.figure(figsize=(6, 6))
    
    
    # all
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
    # plt.plot(x_data, y_data, 'o', color='c', linestyle='None')
    x1_range = np.linspace(MIN, int(intersection), int(intersection)-MIN+1).reshape(-1, 1)
    y1_log_range = model_before1.predict(np.log(x1_range))
    x2_range = np.linspace(int(intersection), MAX, MAX-int(intersection)+1).reshape(-1, 1)
    y2_log_range = model_before2.predict(np.log(x2_range))
    plt.plot(x1_range, np.exp(y1_log_range), 'k', label='all')
    plt.plot(x2_range, np.exp(y2_log_range), 'k')
    
    # frame
    frame_size = 50
    for P, delta in zip(Ps, deltas):
        if P <= intersection: y = np.exp(model_before1.predict(np.log(np.array(P).reshape(1, 1))))
        else: y = np.exp(model_before2.predict(np.log(np.array(P).reshape(1, 1))))
        plt.plot([P, P], [y-frame_size, y+frame_size], 'k', linestyle='--', marker='_')
        # plt.plot([P, P], [delta-frame_size, delta+frame_size], 'r', linestyle='dotted', marker='_')
    # plt.plot(x1_range, np.exp(y1_log_range)-frame_size, 'b', linestyle='dotted', label='$\it{T}-\Delta\it{T}$ 50ms')
    # plt.plot(x2_range, np.exp(y2_log_range)-frame_size, 'b', linestyle='dotted')
    # plt.plot(x1_range, np.exp(y1_log_range)+frame_size, 'b', linestyle='dotted')
    # plt.plot(x2_range, np.exp(y2_log_range)+frame_size, 'b', linestyle='dotted')
    # plt.plot(x1_range, np.exp(y1_log_range)-frame_size*2, 'b', linestyle='dotted', label='$\it{T}-\Delta\it{T}$ 100ms')
    # plt.plot(x2_range, np.exp(y2_log_range)-frame_size*2, 'b', linestyle='dotted')
    # plt.plot(x1_range, np.exp(y1_log_range)+frame_size*2, 'b', linestyle='dotted')
    # plt.plot(x2_range, np.exp(y2_log_range)+frame_size*2, 'b', linestyle='dotted')
    
    # dls
    speech_before_1000 = [75.96541701629783, 77.6752388643372, 75.13647528563304, 92.25641658212591, 118.97786712641043, 132.57432923754584, 262.6385707137894]
    speech_before_1500 = [97.0373920512198, 108.66145439082159, 103.3078746804729, 114.17909012826324, 143.75561544059903, 182.26503802124617, 286.7991143646163]
    speech_after_1000 = [74.10851365606159, 78.6395770358463, 81.05930144476811, 77.24174967472355, 93.71431421611423, 102.42990206086385, 156.0363597117294]
    speech_after_1500 = [77.57789144960687, 87.79440956611133, 86.67537609458797, 83.72033915643979, 98.79721115189075, 106.85333470267246, 177.11344816047298]
    plt.plot(Ps, speech_before_1000, marker='o', color='#9999FF', linestyle='None', label='$\it{T}-\Delta\it{T}$/1000ms')
    plt.plot(Ps, speech_before_1500, marker='o', color='#3333FF', linestyle='None', label='$\it{T}-\Delta\it{T}$/1500ms')
    plt.plot(Ps, speech_after_1000, marker='o', color='#FF9999', linestyle='None', label='$\it{T}+\Delta\it{T}$/1000ms')
    plt.plot(Ps, speech_after_1500, marker='o', color='#FF3333', linestyle='None', label='$\it{T}+\Delta\it{T}$/1500ms')
    
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)  
    plt.xlim(10, 1000)
    plt.ylim(40, 400)
    plt.xlabel("物理時間 $\it{t}$ [ms]", fontsize=15)
    plt.ylabel("弁別閾 $\Delta\it{T}_{\it{DL}}$ [ms]", fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    plt.legend(fontsize=10, title="間隔の長短/信号長", loc='upper left')
    plt.tight_layout()
    #plt.tick_params(labelsize=15)
    plt.savefig(os.path.join(IMGDIR, f'dl_linear_frame1.png'))
    plt.show()


if __name__ == '__main__':
    main()