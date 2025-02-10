import os
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# python check_selections_num_boxplot.py
OUTPUTDIR = '/Users/user/Desktop/授業/lab/資料/知覚実験2/output_v2'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img'


def set_boxplot(box):
    for median in box['medians']:
        median.set_color('b')
    for mean in box['means']:
        mean.set_markerfacecolor('black')
        mean.set_marker('x')
        

def prob():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # output data
    names = os.listdir(OUTPUTDIR)
    names = [name for name in names if name != '.DS_Store']
    
    # test
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    max_deltas = [200, 200, 200, 200, 200, 400, 800]
    all_keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    N = 9
    M = 800
    MIN = 0
    MAX = 1500
    
    # output list
    output_dict = {}
    list_deltas = {}
    all_probs = []
    for max_delta, P in zip(max_deltas, Ps):
        list_deltas[P] = [-1]
        for i in range(N):
            list_deltas[P].append(max_delta/(math.sqrt(2)**(N-i-1)))
    # plt.figure(figsize=(12, 8))
    plt.figure(figsize=(6, 6))
    for name in names:
        namedir = os.path.join(OUTPUTDIR, name)
        output_dict[name] = []
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                # if delta == -1: print(sl, wavlen, P, delta)
                closest_idx = min(range(len(list_deltas[P])), key=lambda j: abs(list_deltas[P][j] - delta))
                output_dict[name].append(closest_idx)
        count = Counter(output_dict[name])
        total_elements = len(output_dict[name])
        probs = {key: value / total_elements for key, value in count.items()}
        for key in all_keys:
            if key not in probs: probs[key] = 0
        sorted_probs = [probs[key] for key in sorted(probs)]
        all_probs.append(sorted_probs)
    num_probs = [[] for _ in range(N+1)]
    for probs in all_probs:
        for i, prob in enumerate(probs):
            num_probs[i].append(prob)
    box = plt.boxplot(num_probs[1:], positions=all_keys[1:], patch_artist=True, sym="")#, showmeans=True)
    set_boxplot(box)
    for patch in box['boxes']:
        patch.set_facecolor('lightblue') # tab:blue
    # for probs in all_probs:
    #     if probs[0] != 0:
    #         print(probs)
    #         plt.plot(all_keys, probs) 
    plt.xlabel('Number', fontsize=15)
    plt.ylabel('Probability', fontsize=15)
    plt.tick_params(axis='both', labelsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'choice_boxplot.png'))
    plt.show()


def set_boxplot(box):
    for median in box['medians']:
        median.set_color('b')
    for mean in box['means']:
        mean.set_markerfacecolor('black')
        mean.set_marker('x')
        

def num():
    
    # make imgdir
    os.makedirs(IMGDIR, exist_ok=True)
    
    # output data
    names = os.listdir(OUTPUTDIR)
    names = [name for name in names if name != '.DS_Store']
    
    # test
    Ps = [12.5, 25, 50, 100, 200, 400, 800]
    max_deltas = [200, 200, 200, 200, 200, 400, 800]
    all_keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    N = 9
    M = 800
    MIN = 0
    MAX = 1500
    
    # output list
    output_dict = {}
    list_deltas = {}
    all_probs = []
    for max_delta, P in zip(max_deltas, Ps):
        list_deltas[P] = [-1]
        for i in range(N):
            list_deltas[P].append(max_delta/(math.sqrt(2)**(N-i-1)))
    # plt.figure(figsize=(12, 8))
    plt.figure(figsize=(6, 6))
    for name in names:
        namedir = os.path.join(OUTPUTDIR, name)
        output_dict[name] = []
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                # if delta == -1: print(sl, wavlen, P, delta)
                closest_idx = min(range(len(list_deltas[P])), key=lambda j: abs(list_deltas[P][j] - delta))
                output_dict[name].append(closest_idx)
        count = Counter(output_dict[name])
        probs = {key: value for key, value in count.items()}
        for key in all_keys:
            if key not in probs: probs[key] = 0
        sorted_probs = [probs[key] for key in sorted(probs)]
        all_probs.append(sorted_probs)
    num_probs = [[] for _ in range(N+1)]
    for probs in all_probs:
        for i, prob in enumerate(probs):
            num_probs[i].append(prob)
    box = plt.boxplot(num_probs[1:], positions=all_keys[1:], patch_artist=True, sym="")#, showmeans=True)
    set_boxplot(box)
    for patch in box['boxes']:
        patch.set_facecolor('lightblue') # tab:blue
    # for probs in all_probs:
    #     if probs[0] != 0:
    #         print(probs)
    #         plt.plot(all_keys, probs) 
    plt.xlabel('Number', fontsize=15)
    plt.ylabel('Count', fontsize=15)
    plt.yticks([5, 10, 15, 20])
    plt.tick_params(axis='both', labelsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'choice_boxplot.png'))
    plt.show()


if __name__ == '__main__':
    # prob()
    num()