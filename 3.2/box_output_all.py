import os
import math
import japanize_matplotlib
import matplotlib.pyplot as plt


# python 3.2/box_output_all.py
OUTPUT1DIR = '/Users/user/Desktop/授業/lab/資料/知覚実験/output_/test1'
OUTPUT2DIR = '/Users/user/Desktop/授業/lab/資料/知覚実験/output_/test2'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img/3.2'


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
    
    # test
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    wavlens = [1000, 1500, 2000]
    outdirs = [OUTPUT1DIR, OUTPUT2DIR]
    N = 9
    M = 800
    NA = 1e10
    
    # output list
    # output1
    output1_before_dict = {}
    output1_after_dict = {}
    output2_before_dict = {}
    output2_after_dict = {}
    for wavlen in wavlens:
        output1_before_dict[wavlen] = {}
        output1_after_dict[wavlen] = {}
        output2_before_dict[wavlen] = {}
        output2_after_dict[wavlen] = {}
        for P in Ps:
            output1_before_dict[wavlen][P] = []
            output1_after_dict[wavlen][P] = []
            output2_before_dict[wavlen][P] = []
            output2_after_dict[wavlen][P] = []
    for i, outdir in enumerate(outdirs):
        names = os.listdir(outdir)
        names = [name for name in names if name != '.DS_Store']
        for name in names:
            namedir = os.path.join(outdir, name)
            with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
                for line in file:
                    sl, wavlen, P, delta = line.split(' ')
                    sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                    if delta == -1: continue
                    if i == 0:
                        if sl == 0: output1_before_dict[wavlen][P].append(delta)
                        else: output1_after_dict[wavlen][P].append(delta)
                    else:
                        if sl == 0: output2_before_dict[wavlen][P].append(delta)
                        else: output2_after_dict[wavlen][P].append(delta)

    # plt
    fig, axes = plt.subplots(2, 1, figsize=(9, 12))#, sharex=True)
    
    # 上
    offset = 8  # 各信号長の箱ひげ図の間隔
    base_position = 1  # 初期位置
    test_dicts = [output1_before_dict, output1_after_dict]
    test_labels = ['無/$\it{T}-\Delta\it{T}$/1000ms', '無/$\it{T}-\Delta\it{T}$/1500ms', '無/$\it{T}-\Delta\it{T}$/2000ms', '無/$\it{T}+\Delta\it{T}$/1000ms', '無/$\it{T}+\Delta\it{T}$/1500ms', '無/$\it{T}+\Delta\it{T}$/2000ms']
    colors = ['#9999FF', '#3333FF', '#000099', '#FF9999', '#FF3333', '#990000']
    all_data = []
    all_positions = []
    for i, P in enumerate(Ps):
        for j, test_dict in enumerate(test_dicts):
            for k, wavlen in enumerate(wavlens):
                all_data.append(test_dict[wavlen][P])
                all_positions.append(base_position + offset * i + j * 3 + k)
    box = axes[0].boxplot(all_data, positions=all_positions, patch_artist=True, sym="")
    set_boxplot(box)
    legend_handles = []
    for i, patch in enumerate(box['boxes']):
        patch.set_facecolor(colors[i%len(colors)])
    for i, (color, label) in enumerate(zip(colors, test_labels)):
        legend_handles.append(plt.Line2D([0], [0], color=color, lw=2, label=label))
    middle_indices = [base_position + offset * i + 2.5 for i in range(len(Ps))]
    axes[0].set_xticks(middle_indices, [P for P in Ps])
    axes[0].set_yscale('log')
    axes[0].set_ylim(0.5, 1000)
    axes[0].tick_params(axis='x', labelsize=13)
    axes[0].tick_params(axis='y', labelsize=13)
    axes[0].set_xlabel('基準値 $T$', fontsize=15)
    axes[0].set_ylabel('弁別閾 $\Delta\it{T}_{choice}$', fontsize=15)
    # axes[0].set_title('実験2.2', fontsize=15)
    axes[0].legend(handles=legend_handles, title="信号の重なり/ずれの方向/信号長D")
    axes[0].grid(True)
    
    # 下
    # offset = 10  # 各信号長の箱ひげ図の間隔
    offset = 5
    base_position = 1  # 初期位置
    wavlen2s = [1000, 1500, 2000]
    test_dict = output2_before_dict
    test_labels = ['有/$\it{T}-\Delta\it{T}$/1000ms', '有/$\it{T}-\Delta\it{T}$/1500ms', '有/$\it{T}-\Delta\it{T}$/2000ms']
    colors = ['#9999FF', '#3333FF', '#000099']
    all_data = []
    all_positions = []
    all_data = []
    all_positions = []
    # Ps = [12.5, 25, 50, 100]
    for i, P in enumerate(Ps):
        for k, wavlen in enumerate(wavlen2s):
            all_data.append(test_dict[wavlen][P])
            all_positions.append(base_position + offset * i + k)
    box = axes[1].boxplot(all_data, positions=all_positions, patch_artist=True, sym="")
    set_boxplot(box)
    legend_handles = []
    for i, patch in enumerate(box['boxes']):
        patch.set_facecolor(colors[i%len(colors)])
    for i, (color, label) in enumerate(zip(colors, test_labels)):
        legend_handles.append(plt.Line2D([0], [0], color=color, lw=2, label=label, linestyle='-'))
    middle_indices = [base_position + offset * i + 1.0 for i in range(len(Ps))]
    axes[1].set_xticks(middle_indices, [P for P in Ps])
    axes[1].set_yscale('log')
    axes[1].set_ylim(0.5, 1000)
    axes[1].tick_params(axis='x', labelsize=13)
    axes[1].tick_params(axis='y', labelsize=13)
    axes[1].set_xlabel('基準長 $T$', fontsize=15)
    axes[1].set_ylabel('弁別閾 $\Delta\it{T}_{choice}$', fontsize=15)
    # axes[1].set_title('実験2.3', fontsize=15)
    axes[1].legend(handles=legend_handles, title="信号の重なり/ずれの方向/信号長D")
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'boxplot_expall.png'))
    plt.show()


if __name__ == "__main__":
    main()