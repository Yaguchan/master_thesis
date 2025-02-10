import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.linear_model import LinearRegression


# python 3.3/dl_frame.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def main():
    
    # ms -> s
    M = 1000
    MIN = 10
    MAX = 1000
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    deltas = [  [85.59902890784883, 90.55002075837777, 88.00614635523516, 101.80761716892818, 131.13026377220612, 155.36261848107216, 274.75263372818694],
                [75.86212923797203, 83.14042457443703, 83.76669469613213, 80.08673514903063, 96.59977644563843, 104.56349686246709, 167.1477317420702]]
    x_range = np.linspace(MIN, MAX, MAX-MIN+1)
    x_data = np.array(Ps).reshape(-1, 1)
    plt.figure(figsize=(6, 6))
    
    for deltas_ in deltas:
        for delta, P in zip(deltas_, Ps):
            print(delta/P)
        print()
    
    # dls
    speech_before_1000 = [75.96541701629783, 77.6752388643372, 75.13647528563304, 92.25641658212591, 118.97786712641043, 132.57432923754584, 262.6385707137894]
    speech_before_1500 = [97.0373920512198, 108.66145439082159, 103.3078746804729, 114.17909012826324, 143.75561544059903, 182.26503802124617, 286.7991143646163]
    speech_after_1000 = [74.10851365606159, 78.6395770358463, 81.05930144476811, 77.24174967472355, 93.71431421611423, 102.42990206086385, 156.0363597117294]
    speech_after_1500 = [77.57789144960687, 87.79440956611133, 86.67537609458797, 83.72033915643979, 98.79721115189075, 106.85333470267246, 177.11344816047298]

    # frame(50ms) range
    frame_size = 50
    # for P, delta in zip(Ps, speech_before_1000):
    #     plt.plot([P, P], [delta-frame_size, delta+frame_size], '#9999FF', linestyle='--', marker='_')
    # for P, delta in zip(Ps, speech_before_1500):
    #     plt.plot([P, P], [delta-frame_size, delta+frame_size], '#3333FF', linestyle='--', marker='_')
    for P, delta in zip(Ps, speech_after_1000):
        plt.plot([P, P], [delta-frame_size, delta+frame_size], '#FF9999', linestyle='--', marker='_')
    for P, delta in zip(Ps, speech_after_1500):
        plt.plot([P, P], [delta-frame_size, delta+frame_size], '#FF3333', linestyle='--', marker='_')
        
    # plt
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
    plt.savefig(os.path.join(IMGDIR, f'dl_speech_frame.png'))
    plt.show()


if __name__ == '__main__':
    main()