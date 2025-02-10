import os
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment, silence
from pydub.silence import detect_silence, detect_nonsilent


# python check_pause.py
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img'


def audio_to_array(audio_segment):
    """pydub AudioSegment を NumPy 配列に変換"""
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))  # ステレオ音声の場合
    return samples


def normalize_amplitude(data):
    """振幅を -1 ～ 1 に正規化する"""
    max_amplitude = np.max(np.abs(data))  # 波形データの最大振幅（絶対値）
    return data / max_amplitude if max_amplitude != 0 else data


def detect_pause(nonsilent_ranges, point):
    for idx, (start, end) in enumerate(nonsilent_ranges):
        if start > point: 
            return nonsilent_ranges[idx-1][1], nonsilent_ranges[idx][0]
    return -1, -1


def main():
    # params
    silence_thresh = -80
    min_silence_len = 1
    wavpaths = [
        '/Users/user/Desktop/授業/lab/学会/音響処理学会2025春/論文/wav/vs/tone_1000_100_0.wav',
        '/Users/user/Desktop/授業/lab/学会/音響処理学会2025春/論文/wav/vs/tone_1500_100_0.wav',
        '/Users/user/Desktop/授業/lab/学会/音響処理学会2025春/論文/wav/vs/utterance_1000_100_0.wav',
        '/Users/user/Desktop/授業/lab/学会/音響処理学会2025春/論文/wav/vs/utterance_1500_100_0.wav'
    ]
    labels = [
        '純音 D=1000',
        '純音 D=1500',
        '音声 D=1000',
        '音声 D=1500',
    ]
    points = [1000+500, 1500+500, 1000+500, 1500+500]
    fig, axes = plt.subplots(len(wavpaths), 1, figsize=(6, 6))
    for ax, wavpath, point, label in zip(axes, wavpaths, points, labels):
        audio = AudioSegment.from_file(wavpath)
        nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
        start, end = detect_pause(nonsilent_ranges, point)
        print(end-start)
        array = normalize_amplitude(audio_to_array(audio))
        time = np.linspace(0, len(array) / audio.frame_rate, num=len(array))
        ax.plot(time*1000, array, color='b')
        ax.axvline(start, color='r', linestyle='--', label=f'{silence_thresh}dBFS, len={end-start}[ms]')
        ax.axvline(end, color='r', linestyle='--')
        ax.set_title(label)
        ax.set_ylabel("Amplitude")
        ax.set_xlim(450, 4000)
        ax.grid()
        ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'{silence_thresh}dBFS_pause.png'))
    plt.show()
    

if __name__ == '__main__':
    main()