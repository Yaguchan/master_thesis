import os
import japanize_matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


# python compare_wav.py
WAV1PATH = '/Users/user/Desktop/授業/lab/学会/音響処理学会2025春/論文/wav/vs/tone_1000_100_0.wav'
WAV2PATH = '/Users/user/Desktop/授業/lab/学会/音響処理学会2025春/論文/wav/vs/utterance_1000_100_0.wav'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img'


def main():
    # 音声ファイルの読み込み
    sample_rate_a, data_a = wavfile.read(WAV1PATH)
    sample_rate_b, data_b = wavfile.read(WAV2PATH)
    
    # 振幅を正規化 (-1 から 1 にスケーリング)
    data_a = data_a / np.max(np.abs(data_a))
    data_b = data_b / np.max(np.abs(data_b))

    # 時間軸の作成
    time_a = [i / sample_rate_a * 1000 for i in range(len(data_a))]
    time_b = [i / sample_rate_b * 1000 for i in range(len(data_b))]

    # プロット設定
    fig, axs = plt.subplots(2, 1, figsize=(12, 4), sharex=True)

    # A.wavのプロット
    axs[0].plot(time_a, data_a, color='c')
    axs[0].set_title('純音 D=1000')
    axs[0].set_ylabel('Amplitude')
    axs[0].tick_params(axis='both', labelsize=13)

    # B.wavのプロット
    axs[1].plot(time_b, data_b, color='m')
    axs[1].set_title('音声「おはようございます」D=1000')
    axs[1].set_xlabel('Time [ms]')
    axs[1].set_ylabel('Amplitude')
    axs[1].tick_params(axis='both', labelsize=13)

    # 全体の調整
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'tone_audio.png'))
    plt.show()


if __name__ == '__main__':
    main()