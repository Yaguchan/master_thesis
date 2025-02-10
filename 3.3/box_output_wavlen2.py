import os
import math
import japanize_matplotlib
import matplotlib.pyplot as plt


# python box_output_wavlen2.py
OUTPUTDIR = '/Users/user/Desktop/授業/lab/資料/知覚実験2/output_v2'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img'


def set_boxplot(box):
    for median in box['medians']:
        median.set_color('y')
    for mean in box['means']:
        mean.set_markerfacecolor('black')
        mean.set_marker('x')


def main():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # output data
    names = os.listdir(OUTPUTDIR)
    names = [name for name in names if name != '.DS_Store']
    
    # test
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    max_deltas = [200, 200, 200, 200, 200, 400, 800]
    wavlens = [1000, 1500, 2000]
    colors = ['b', 'g', 'y']
    N = 9
    M = 800
    
    # output list
    output_before_dict = {}
    output_after_dict = {}
    for wavlen in wavlens:
        output_before_dict[wavlen] = {}
        output_after_dict[wavlen] = {}
        for P in Ps:
            output_before_dict[wavlen][P] = []
            output_after_dict[wavlen][P] = []
    
    for name in names:
        namedir = os.path.join(OUTPUTDIR, name)
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                if delta == -1: continue
                if sl == 0:
                    output_before_dict[wavlen][P].append(delta)
                else:
                    output_after_dict[wavlen][P].append(delta)
    
    # plt
    plt.subplots(figsize=(12, 6))
    offset = 8  # 各信号長の箱ひげ図の間隔
    base_position = 1  # 初期位置
    all_data = []
    all_positions = []
    # colors = ['r', 'g', 'b', 'darkred', 'darkgreen', 'darkblue']
    colors = ['#FFAAAA', '#A3CFFF', '#A8E6A3', '#D32F2F', '#1976D2', '#388E3C']
    test_dicts = [output_before_dict, output_after_dict]
    img_names = ['P-Δ', 'P+Δ']
    for i, P in enumerate(Ps):
        for j, test_dict in enumerate(test_dicts):
            for k, wavlen in enumerate(wavlens):
                all_data.append(test_dict[wavlen][P])
                all_positions.append(base_position + offset * i + j * 3 + k)
    box = plt.boxplot(all_data, positions=all_positions, patch_artist=True, sym="")
    set_boxplot(box)
    legend_handles = [] 
    for i, patch in enumerate(box['boxes']):
        patch.set_facecolor(colors[i%len(colors)])
    for i, color in enumerate(colors):
        sl = i // 3
        num = i % 3
        legend_handles.append(plt.Line2D([0], [0], color=color, lw=2, label=f'{img_names[sl]} {wavlens[num]}[ms]'))
    middle_indices = [base_position + offset * i + 2.5 for i in range(len(Ps))]
    plt.xticks(middle_indices, [P for P in Ps])
    plt.yscale('log')
    plt.ylim(10, 1000)
    plt.tick_params(axis='x', labelsize=12)
    plt.tick_params(axis='y', labelsize=12)
    plt.xlabel('P', fontsize=13)
    plt.ylabel('Δ', fontsize=13)
    plt.legend(handles=legend_handles, title="ずれの方向/信号長D")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'boxplot_.png'))
    plt.show()


if __name__ == "__main__":
    main()