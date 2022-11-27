import numpy as np
import os
import librosa
import json
import fft
import plot
from parameters import *
import peakpicker as pp
import fingerprint as fhash
from os import environ


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


if __name__ == '__main__':
    suppress_qt_warnings()

    database = np.zeros((1,5))
    id2name = {}
    song_list = os.listdir("./database/正常")

    for i in range(len(song_list)):

        # 获取歌名
        songname = song_list[i].split(".")[0]

        # 计算频谱图
        print("正在分析：" + song_list[i] + "......")
        y, sr = librosa.load("./database/正常/" + song_list[i], sr=SAMPLE_RATE)
        spectrogram = fft.stft(y, WINDOW_SIZE, WINDOW_SHIFT) # 快速傅里叶变换，得到频谱图

        # 挑选峰值点
        threshold = pp.find_thres(spectrogram, percentile, base)
        peaks = pp.peak_pick(spectrogram, f_dim1, t_dim1, f_dim2, t_dim2, threshold, base)
        print("得到峰值点数量：" + str(len(peaks)))
        peaks = pp.reduce_peaks(peaks, FFT_SIZE, high_peak_threshold, low_peak_threshold)
        print("删减后峰值点数量：" + str(len(peaks)))

        # 绘制频谱图和峰值点
        plot.plot_spectrogram_(spectrogram, songname)
        plot.plot_spectrogram(spectrogram, peaks, songname)

        # 计算哈希矩阵
        hashMatrix = fhash.hashPeaks(peaks, i, delay_time, delta_time, delta_freq)

        # 添加到哈希数据库
        database = np.concatenate((database, hashMatrix), axis=0)

        # 记录下歌曲id和歌名对
        id2name[i] = song_list[i].split(".")[0]

    print('得到哈希数据库的大小：'+str(database.shape))
    database = database[np.lexsort((database[:,2],database[:,1],database[:,0]))]

    # 保存中间结果
    np.save("middle_results/database.npy", database)
    with open("middle_results/id2name.json", 'w') as f:
        json.dump(id2name, f)
