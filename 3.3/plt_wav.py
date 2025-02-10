import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment, silence
from pydub.silence import detect_silence, detect_nonsilent


# python plt_wav.py
# MP3PATH = '/Users/user/Desktop/授業/lab/対話班ゼミ/2024/1224/code/wav_practice/ohayougozaimasu/mp3/anaB.mp3'
MP3PATH = '/Users/user/Desktop/授業/lab/学会/音響処理学会2025春/論文/wav/mp3/ohayou/anaA.mp3'
IMGDIR = '/Users/user/Desktop/授業/lab/卒修論/修論/img'
TARGETMS = 1000


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


def adjust_speed(audio_segment, speed=1.0):
    """音声の速度を調整する"""
    new_frame_rate = int(audio_segment.frame_rate * speed)
    return audio_segment._spawn(audio_segment.raw_data, overrides={"frame_rate": new_frame_rate}).set_frame_rate(audio_segment.frame_rate)


def main():
    
    # パラメータ
    silence_thresh = -50    # dBFS
    min_silence_len = 1     # ミリ秒

    # 音声の読み込み
    audio = AudioSegment.from_file(MP3PATH, format='mp3')
    audio.export(MP3PATH.replace('.mp3', '.wav'), format="wav")

    # 無音部分の検出
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    if nonsilent_ranges:
        start_trim = nonsilent_ranges[0][0]  # 最初の無音区間の終了位置
        end_trim = nonsilent_ranges[-1][1]  # 最後の無音区間の開始位置

    # 切り出し/速度調整
    trimmed_audio = audio[start_trim:end_trim]
    current_duration_ms = len(trimmed_audio)
    speed = current_duration_ms / TARGETMS
    adjusted_audio = adjust_speed(trimmed_audio, speed=speed)

    # 元の波形データ
    original_array = normalize_amplitude(audio_to_array(audio))
    original_time = np.linspace(0, len(original_array) / audio.frame_rate, num=len(original_array))

    # 切り出し後の波形データ
    trimmed_array = normalize_amplitude(audio_to_array(trimmed_audio))
    trimmed_time = np.linspace(start_trim, end_trim, num=len(trimmed_array))

    # 速度調整後の波形データ
    adjusted_array = normalize_amplitude(audio_to_array(adjusted_audio))
    adjusted_time = np.linspace(0, TARGETMS, num=len(adjusted_array))

    # プロット
    fig, axs = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

    # 元の波形
    print(start_trim, end_trim)
    axs[0].plot(original_time*1000, original_array, color='k')
    axs[0].plot(original_time[:end_trim*audio.frame_rate//1000]*1000, original_array[:end_trim*audio.frame_rate//1000], color='c', label=f'×1.0(D={end_trim}ms)')
    axs[0].plot(original_time[:start_trim*audio.frame_rate//1000]*1000, original_array[:start_trim*audio.frame_rate//1000], color='k')
    axs[0].axvline(start_trim, color='r', linestyle='--', label=f'{silence_thresh}dBFS')
    axs[0].axvline(end_trim, color='r', linestyle='--')
    axs[0].set_title("Original Audio")
    # axs[0].xlabel("Time [s]")
    axs[0].set_ylabel("Amplitude")
    axs[0].set_xlim(-50, len(original_time)/audio.frame_rate * 1000)
    axs[0].grid()
    axs[0].legend()

    # 速度調整後の波形
    axs[1].plot(adjusted_time, adjusted_array, color='c', label=f'×{speed}(D={TARGETMS}ms)')
    axs[1].axvline(0, color='r', linestyle='--', label=f'{silence_thresh}dBFS')
    axs[1].axvline(len(adjusted_time)/audio.frame_rate*1000, color='r', linestyle='--')
    axs[1].set_title("Adjusted Audio")
    axs[1].set_xlabel("Time [ms]")
    axs[1].set_ylabel("Amplitude")
    axs[1].set_xlim(-50, len(original_time)/audio.frame_rate*1000)
    axs[1].grid()
    axs[1].legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, f'cut_audio.png'))
    plt.show()


if __name__ == '__main__':
    main()