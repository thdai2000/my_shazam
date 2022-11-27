import os
import numpy as np
import librosa
import json
import fft
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
    numSongs = len(id2name)

    # 解析命令行输入
    parser = argparse.ArgumentParser(description='Evaluate retrieval accuracy.')
    parser.add_argument('--type', type=str, help='正常/噪声')
    parser.add_argument('--len', type=str, help='5s/10s/20s')
    parser.add_argument('--vote', type=str, help='匹配哈希数/相同时间差')
    opt = parser.parse_args()


    sample_num = len(os.listdir("query/"+opt.type+"/"+opt.len))
    acc_num = 0

    for query in os.listdir("query/"+opt.type+"/"+opt.len):

        query_path = "query/"+opt.type+"/"+opt.len+"/"+query
        songname = query.split("_")[0] + "_" + query.split("_")[1]
        print("正在分析" + query + "......")
        y, sr = librosa.load(query_path, sr=SAMPLE_RATE)
        spectrogram = fft.stft(y, WINDOW_SIZE, WINDOW_SHIFT)

        # 挑选峰值点
        threshold = pp.find_thres(spectrogram, percentile, base)
        peaks = pp.peak_pick(spectrogram, f_dim1, t_dim1, f_dim2, t_dim2, threshold, base)
        peaks = pp.reduce_peaks(peaks, FFT_SIZE, high_peak_threshold, low_peak_threshold)

        # 计算哈希矩阵
        hashSample = fhash.hashSamplePeaks(peaks,delay_time,delta_time,delta_freq)

        # 与哈希库进行匹配，并得到时间对
        timepairs = fhash.findTimePairs(database, hashSample, TPdelta_freq, TPdelta_time)

        predict_idx = -1
        if opt.vote == "匹配哈希数":

            # 统计匹配到的哈希的歌曲ID
            numSongs = len(id2name)
            songbins= np.zeros(numSongs)
            for pair in timepairs:
                offset = pair[1] - pair[2]
                songbins[int(pair[2])] += 1

            # 获取歌曲ID
            predict_idx = np.argmax(songbins)

        else:

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

            # 获取歌曲ID
            predict_idx = np.argmax(maxnums)

        # 推断样本歌曲
        if predict_idx == -1:
            print("未能识别")
            continue
        else:
            print('推断该歌曲为：' + id2name[str(predict_idx)])

        if id2name[str(predict_idx)] == songname:
            acc_num += 1

    print('准确率为：' + str(acc_num/sample_num))
