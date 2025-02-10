import numpy as np

# python cal_crosspoint.py
def main():
    # y = a * n ^ b
    # 音声
    # a1 = 70.9
    # n1 = 0.0709
    # a2 = 7.26
    # n2 = 0.534
    # a1 = 73.9
    # n1 = 0.0245
    # a2 = 11.1
    # n2 = 0.396
    # 純音
    # a1 = 39.4
    # n1 = 0.0838
    # a2 = 0.281
    # n2 = 1.04
    a1 = 39.2
    n1 = 0.158
    a2 = 18.6
    n2 = 0.317
    cross_point = np.exp(np.log(a1/a2)/(n2-n1))
    print(f'交点: {cross_point}')

if __name__ == '__main__':
    main()