import os
import math
import japanize_matplotlib
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.linear_model import LinearRegression


# python 3.3/dl_research.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.3'


def mid_log(x, y):
    return np.exp((np.log(x)+np.log(y))/2)


def main():
    
    # データ
    # Getty
    getty_lens = [50, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2400, 2800, 3200]
    xs = [
        [35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65],\
        [75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125],\
        [160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240],\
        [350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450],\
        [500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700],\
        [650, 680, 710, 740, 770, 800, 830, 860, 890, 920, 950],\
        [900, 920, 940, 960, 980, 1000, 1020, 1040, 1060, 1080, 1100],\
        [1075, 1100, 1125, 1150, 1175, 1200, 1225, 1250, 1275, 1300, 1325],\
        [1250, 1280, 1310, 1340, 1370, 1400, 1430, 1460, 1490, 1520, 1550],\
        [1400, 1440, 1480, 1520, 1560, 1600, 1640, 1680, 1720, 1760, 1800],\
        [1600, 1640, 1680, 1720, 1760, 1800, 1840, 1880, 1920, 1960, 2000],\
        [1800, 1840, 1880, 1920, 1960, 2000, 2040, 2080, 2120, 2160, 2200],\
        [1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900],\
        [2050, 2200, 2350, 2500, 2650, 2800, 2950, 3100, 3250, 3400, 3550],\
        [2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4200],\
    ]
    # D.G.
    dg_ps = [
        [0, 0, 0, 0.2, 0.4, 0.6, 0.76, 1.00, 0.96, 1.00, 1.00],\
        [0, 0.04, 0, 0.04, 0.36, 0.52, 0.64, 0.96, 1.00, 1.00, 1.00],\
        [0, 0, 0, 0.12, 0.28, 0.72, 0.80, 0.96, 1.00, 1.00, 1.00],\
        [0, 0, 0.04, 0.04, 0.24, 0.68, 0.84, 0.92, 0.92, 1.00, 1.00],\
        [0, 0, 0, 0.08, 0.04, 0.64, 0.72, 0.96, 0.96, 0.96, 1.00],\
        [0, 0, 0, 0.08, 0.28, 0.48, 0.80, 1.00, 1.00, 1.00, 1.00],\
        [0, 0, 0.12, 0.28, 0.68, 0.56, 0.88, 0.84, 0.88, 1.00, 0.96],\
        [0, 0.12, 0.16, 0.28, 0.28, 0.72, 0.56, 0.88, 0.88, 0.88, 0.96],\
        [0.04, 0.04, 0.16, 0.08, 0.36, 0.56, 0.60, 0.88, 0.80, 1.00, 0.88],\
        [0, 0, 0.12, 0.16, 0.44, 0.72, 0.76, 0.80, 0.96, 0.96, 0.96],\
        [0, 0.04, 0, 0.20, 0.16, 0.72, 0.84, 0.76, 0.92, 0.96, 1.00],\
        [0, 0.16, 0.12, 0.32, 0.36, 0.52, 0.68, 0.80, 0.92, 0.96, 1.00],\
        [0, 0.04, 0, 0.16, 0.52, 0.84, 0.88, 0.96, 0.96, 1.00, 1.00],\
        [0, 0, 0.12, 0.12, 0.32, 0.54, 0.68, 0.96, 1.00, 1.00, 1.00],\
        [0, 0.04, 0.08, 0.24, 0.44, 0.44, 0.84, 0.92, 0.88, 1.00, 1.00],\
    ]
    # T.W.
    tw_ps = [
        [0.04, 0.04, 0.20, 0.36, 0.36, 0.48, 0.72, 0.88, 0.88, 0.96, 1.00],\
        [0, 0.12, 0.04, 0.24, 0.48, 0.64, 0.84, 0.88, 1.00, 0.96, 1.00],\
        [0, 0, 0.16, 0.16, 0.60, 0.64, 0.72, 0.84, 0.92, 0.96, 0.96],\
        [0, 0, 0.29, 0.44, 0.80, 0.84, 0.84, 0.92, 1.00, 1.00, 1.00],\
        [0, 0, 0, 0.08, 0.24, 0.52, 0.64, 0.80, 0.88, 1.00, 1.00],\
        [0, 0.04, 0.04, 0.12, 0.44, 0.60, 0.84, 1.00, 1.00, 0.96, 1.00],\
        [0, 0.08, 0.24, 0.24, 0.52, 0.60, 0.84, 0.68, 0.88, 0.96, 0.96],\
        [0.08, 0.08, 0.36, 0.44, 0.72, 0.64, 0.88, 0.84, 0.96, 1.00, 1.00],\
        [0, 0.04, 0.20, 0.32, 0.64, 0.52, 0.84, 0.96, 0.92, 1.00, 0.96],\
        [0.04, 0.12, 0.16, 0.40, 0.48, 0.76, 0.96, 0.96, 0.92, 1.00, 1.00],\
        [0, 0.12, 0.12, 0.40, 0.44, 0.48, 0.60, 0.88, 0.88, 1.00, 0.96],\
        [0.08, 0.24, 0.17, 0.40, 0.32, 0.64, 0.84, 0.76, 0.80, 0.88, 1.00],\
        [0, 0, 0.04, 0.64, 0.60, 0.92, 0.96, 1.00, 1.00, 1.00, 1.00],\
        [0, 0.16, 0.20, 0.20, 0.52, 0.68, 0.88, 0.96, 1.00, 1.00, 1.00],\
        [0, 0, 0.20, 0.32, 0.28, 0.50, 0.80, 0.88, 0.96, 0.96, 0.92],\
    ]
    getty_dls = []
    
    # Halpern
    halpern_lens = [400, 550, 700, 850, 1000, 1150, 1300, 1450]
    halpern_dls = [17.50, 24.21, 24.72, 28.91, 31.00, 36.81, 49.55, 54.16]
    
    # Perner
    # perner_lens = [0.3, 1, 3, 5, 10, 30, 100, 300, 1000]
    # perner_dls = [1.8, 1.7, 0.8, 2.3, 7.5, 14.3, 19.7, 25.3, 70]
    perner_lens = [10, 30, 100, 300, 1000]
    perner_dls = [7.5, 14.3, 19.7, 25.3, 70]

    # NTT
    ntt_lens = [500, 1000, 3000]
    a = 0.4
    Ks = [11.3, 16.4, 31.5]
    # D=500/1000/3000ms
    ntt_500_dls = [120, 165, 370]
    ntt_1000_dls = [176, 300, 475]
    ntt_3000_dls = [280, 400, 700]
    # for ntt_P in ntt_lens:
    #     ntt_500_dls.append(Ks[0]*(ntt_P**a))
    #     ntt_1000_dls.append(Ks[1]*(ntt_P**a))
    #     ntt_3000_dls.append(Ks[2]*(ntt_P**a))
    # print(ntt_500_dls)
    # print(ntt_1000_dls)
    # print(ntt_3000_dls)
        
    # yaguchi 23/07
    yaguchi23_lens = [100, 200, 400, 800, 1600]
    yaguchi23_dls = [30.498747491084664, 33.5328836032993, 53.49648869713307, 85.30547230701862, 160.1816353757621]
    
    # yaguchi tone 24/12
    # b/a
    yaguchi24_lens = [12.5, 25, 50, 100, 200, 400, 800]
    yaguchi24_tone_b_dls = [47.61318743178709, 52.200276025035635, 56.75976440284747, 56.189391873094, 69.44414628430894, 137.0129835929062, 292.569794466654]
    yaguchi24_tone_a_dls = [59.93659322585963, 63.4362614165684, 71.91237226966966, 82.85335970530495, 97.32043936265173, 130.44512657021983, 150.96718510363644]
    # wavlen
    # yaguchi24_tone_b_1000_dls = [44.190644195319315, 42.133228427872076, 49.71979826703801, 53.78584599488387, 69.07161225054475, 104.97903401490792, 255.6789492187238]
    # yaguchi24_tone_b_1500_dls = [43.715526191493325, 50.735330844563265, 56.971946612303135, 58.581395633148425, 66.3906794718752, 156.855186651121, 278.5759867156664]
    # yaguchi24_tone_b_2000_dls = [58.666877871767774, 66.29522843441457, 64.42416095405143, 56.34229464586939, 71.55018109200451, 150.4541241468546, 347.83560572599686]
    # yaguchi24_tone_a_1000_dls = [56.40498897316301, 61.65564953872158, 66.98337637372933, 74.09739279049822, 82.0822608456563, 126.65088957468852, 120.39721968885613]
    # yaguchi24_tone_a_1500_dls = [62.899241191058714, 61.511341394841686, 72.42190421766529, 83.70434228915842, 96.54013789522813, 115.80504939401547, 161.00911706841126]
    # yaguchi24_tone_a_2000_dls = [60.59646243548518, 67.51009579331655, 77.49812528664981, 87.27988724588143, 110.02520688470003, 155.45541955935073, 174.86210478826501]
    
    # yaguchi utterance 24/12
    yaguchi24_utterance_b_dls = [85.59902890784883, 90.55002075837777, 88.00614635523516, 101.80761716892818, 131.13026377220612, 155.36261848107216, 274.75263372818694]
    yaguchi24_utterance_a_dls = [75.86212923797203, 83.14042457443703, 83.76669469613213, 80.08673514903063, 96.59977644563843, 104.56349686246709, 167.1477317420702]
    # 標準正規分布の逆累積分布値を計算
    x_075 = norm.ppf(0.75)  # 0.75 の位置
    x_025 = norm.ppf(0.25)  # 0.25 の位置
    half_range = (x_075 - x_025) / 2
    
    # sd/dlの算出
    getty_list_dls = []
    for ps in [dg_ps, tw_ps]:
        dls = []
        for x, p in zip(xs, ps):
            data = {
                "x": x,
                "p": p
            }
            df = pd.DataFrame(data)
            df = df[df["p"]!=0]
            df = df[df["p"]!=1]
            df["z"] = norm.ppf(df["p"])
            X = np.array(df["x"]).reshape(-1, 1)
            y = df["z"]
            model = LinearRegression().fit(X, y)
            slope = model.coef_[0]
            sd = 1 / slope
            dl = half_range * sd
            dls.append(dl)
        getty_list_dls.append(dls)
    for dl0, dl1 in zip(getty_list_dls[0], getty_list_dls[1]):
        getty_dls.append(mid_log(dl0, dl1))

    # plt
    plt.figure(figsize=(6, 6))
    plt.plot(getty_lens, getty_dls, marker='s', linestyle='dotted', label='Getty [1]')
    # plt.plot(getty_lens, getty_list_dls[0], marker='s', linestyle='--', label='[4] D.G.')                                         # Getty D.G.
    # plt.plot(getty_lens, getty_list_dls[1], marker='s', linestyle='--', label='[4] T.W.')                                         # Getty T.W.
    plt.plot(perner_lens, perner_dls, marker='s', color='y', linestyle='--', label='Perner [2]')                                                    # Perner
    plt.plot(halpern_lens, halpern_dls, marker='s', linestyle='dotted', label='Halpern & Darwin [3]')                               # Halpern
    plt.plot(ntt_lens, ntt_500_dls, marker='s', color='#99FF99', linestyle='dotted', label='伊藤 [4] D=500ms')                                                  # NTT 500
    plt.plot(ntt_lens, ntt_1000_dls, marker='s', color='#33CC33', linestyle='dotted', label='伊藤 [4] D=1000ms')                                                # NTT 1000
    plt.plot(ntt_lens, ntt_3000_dls, marker='s', color='#006600', linestyle='dotted', label='伊藤 [4] D=3000ms')                                                # NTT 500
    plt.plot(yaguchi24_lens, yaguchi24_tone_b_dls, marker='x', color='b', linestyle='--', label='純音/$\it{T}-\Delta\it{T}$/D=1000,1500,2000ms')                      # yaguchi tone -
    plt.plot(yaguchi24_lens, yaguchi24_tone_a_dls, marker='x', color='r', linestyle='--', label='純音/$\it{T}+\Delta\it{T}$/D=1000,1500,2000ms')                      # yaguchi tone +
    # plt.plot(yaguchi24_lens, yaguchi24_tone_b_1000_dls, marker='o', color='lightblue', label='$\it{T}-\Delta\it{T}$ D=1000')     # yaguchi - 1000
    # plt.plot(yaguchi24_lens, yaguchi24_tone_b_1500_dls, marker='o', color='blue', label='$\it{T}-\Delta\it{T}$ D=1500')          # yaguchi - 1500
    # plt.plot(yaguchi24_lens, yaguchi24_tone_b_2000_dls, marker='o', color='darkblue', label='$\it{T}-\Delta\it{T}$ D=2000')      # yaguchi - 2000
    # plt.plot(yaguchi24_lens, yaguchi24_tone_a_1000_dls, marker='s', color='lightsalmon', label='$\it{T}-\Delta\it{T}$, D=1000')  # yaguchi + 1000
    # plt.plot(yaguchi24_lens, yaguchi24_tone_a_1500_dls, marker='s', color='red', label='$\it{T}-\Delta\it{T}$ D=1500')           # yaguchi + 1500
    # plt.plot(yaguchi24_lens, yaguchi24_tone_a_2000_dls, marker='s', color='darkred', label='$\it{T}-\Delta\it{T}$ D=2000')       # yaguchi + 2000
    plt.plot(yaguchi24_lens, yaguchi24_utterance_b_dls, marker='o', color='b', label='音声/$\it{T}-\Delta\it{T}$/D=1000,1500ms')            # yaguchi utterance -
    plt.plot(yaguchi24_lens, yaguchi24_utterance_a_dls, marker='o', color='r', label='音声/$\it{T}+\Delta\it{T}$/D=1000,1500ms')            # yaguchi utterance +
    plt.xlabel("基準値 $\it{T}$ [ms]", fontsize=15)
    plt.ylabel("弁別閾 $\Delta\it{T}_{\it{DL}}$ [ms]", fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    plt.xscale('log')
    plt.yscale('log')
    # plt.legend(loc='upper left', fontsize=10)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'research_dls.png'))
    plt.show()


if __name__ == '__main__':
    main()