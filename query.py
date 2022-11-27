import numpy as np
import librosa
import json
import fft
import plot
from parameters import *
import peakpicker as pp
import fingerprint as fhash
import argparse
from os import environ


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


if __name__ == '__main__':
    suppress_qt_warnings()

    # 加载中间结果
    database = np.load("./middle_results/database.npy")
    with open("./middle_results/id2name.json", "r") as r:
        id2name = json.load(r)

    # 解析命令行输入
    parser = argparse.ArgumentParser(description='Search your song.')
    parser.add_argument('-q', type=str)
    opt = parser.parse_args()

    # 计算检索样本query的频谱图
    query = opt.q
    query_type = query.split("\\")[2]
    query_name = query.split("\\")[-1].split(".")[0]
    print("正在分析" + query_name + "......")
    y, sr = librosa.load(query, sr=SAMPLE_RATE)
    spectrogram = fft.stft(y, WINDOW_SIZE, WINDOW_SHIFT)

    # 挑选峰值点
    threshold = pp.find_thres(spectrogram, percentile, base)
    peaks = pp.peak_pick(spectrogram, f_dim1, t_dim1, f_dim2, t_dim2, threshold, base)
    print("得到峰值点数量：" + str(len(peaks)))
    peaks = pp.reduce_peaks(peaks, FFT_SIZE, high_peak_threshold, low_peak_threshold)
    print("删减后峰值点数量：" + str(len(peaks)))

    # 绘制频谱图和峰值点
    # plot.plot_spectrogram(spectrogram, peaks, query_name)

    # 计算哈希矩阵
    hashSample = fhash.hashSamplePeaks(peaks,delay_time,delta_time,delta_freq)
    print("得到" + str(hashSample.shape[0]) + "个哈希")

    # 与哈希库进行匹配，并得到时间对
    timepairs = fhash.findTimePairs(database, hashSample, TPdelta_freq, TPdelta_time)

    # 统计匹配到的哈希的歌曲ID
    numSongs = len(id2name)
    songbins= np.zeros(numSongs)
    for pair in timepairs:
        offset = pair[1] - pair[2]
        songbins[int(pair[2])] += 1

    # 绘制歌曲识别统计图
    for i in range(len(songbins)):
        print("与" + id2name[str(i)] + "匹配的哈希数：" + str(int(songbins[i])))
    plot.plot_songbins(songbins, numSongs, list(id2name.values()), query_type + "版 " + query_name)

    # 推断样本歌曲
    predict_idx = np.argmax(songbins)
    print('推断该歌曲为：' + id2name[str(predict_idx)])

    # 统计与每一首歌的相同时间差个数的最大值
    offsetbins = {}
    maxnums = np.zeros(numSongs)
    for pair in timepairs:
        if int(pair[2]) not in offsetbins.keys():
            offsetbins[int(pair[2])] = {}
        if int(pair[0]) - int(pair[1]) not in offsetbins[int(pair[2])].keys():
            offsetbins[int(pair[2])][int(pair[0]) - int(pair[1])] = 1
        else:
            offsetbins[int(pair[2])][int(pair[0]) - int(pair[1])] += 1
    for songID, offsets in offsetbins.items():
        maxnum = max(offsets.values())
        maxnums[int(songID)] = maxnum

    # 打印结果
    for i in range(len(maxnums)):
        print("与" + id2name[str(i)] + "的相同时间差的最高出现次数：" + str(int(maxnums[i])))
    plot.plot_maxnums(maxnums, numSongs, list(id2name.values()), query_type + "版 " + query_name)

    # 推断样本歌曲
    predict_idx = np.argmax(maxnums)
    print('推断该歌曲为：' + id2name[str(predict_idx)])
