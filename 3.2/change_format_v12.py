import os
import math
import numpy as np


# python 3.2change_format_v12.py
V1DICT = '/Users/user/Desktop/授業/lab/資料/知覚実験/output'
V2DICT = '/Users/user/Desktop/授業/lab/資料/知覚実験/output_'


def test1():
    wavlens = [1000, 1500, 2000]
    names = os.listdir(V1DICT)
    names = [name for name in names if name != '.DS_Store']
    for name in names:
        os.makedirs(os.path.join(V2DICT, 'test1', name), exist_ok=True)
        path = os.path.join(V2DICT, 'test1', name, f'output_test.txt')
        if os.path.exists(path): os.remove(path)
        with open(path, 'a') as output_file:
            dirpath = os.path.join(V1DICT, name)
            for wavlen in wavlens:
                for sl in [1, 2]:
                    with open(os.path.join(dirpath, f'output1_{wavlen}_{sl}.txt'), 'r') as input_file:
                        for line in input_file:
                            P, delta = line.split(': ')
                            output_file.write(f'{sl-1} {wavlen} {P} {delta}')


def test2():
    wavlens = [1000, 1500, 2000]
    names = os.listdir(V1DICT)
    names = [name for name in names if name != '.DS_Store']
    for name in names:
        os.makedirs(os.path.join(V2DICT, 'test2', name), exist_ok=True)
        path = os.path.join(V2DICT, 'test2', name, f'output_test.txt')
        if os.path.exists(path): os.remove(path)
        with open(path, 'a') as output_file:
            dirpath = os.path.join(V1DICT, name)
            for wavlen in wavlens:
                with open(os.path.join(dirpath, f'output2_{wavlen}.txt'), 'r') as input_file:
                    for line in input_file:
                        P, delta = line.split(': ')
                        output_file.write(f'{0} {wavlen} {P} {delta}')


if __name__ == "__main__":
    # test1()
    test2()