import matplotlib.pyplot as plt
import numpy as np
# pylab.rcParams["font.sans-serif"] = ["SimHei"] # 设置字体
# pylab.rcParams["axes.unicode_minus"] = False # 该语句解决图像中的“-”负号的乱码问题


# 绘制时频谱
def plot_spectrogram_(S, songname):
    fig = plt.figure(figsize=(15, 6))
    plt.imshow(S, origin='lower', aspect='auto', interpolation='nearest', cmap="RdYlGn_r")
    plt.title(songname + ' 时频谱')
    plt.xlabel('时间')
    plt.ylabel('频率块')
    fig.savefig("plots/时频谱 " + songname + ".png")


# 绘制时频谱和峰值点
def plot_spectrogram(S, peaks, songname):
    fig = plt.figure(figsize=(15, 6))
    plt.imshow(S, origin='lower', aspect='auto', interpolation='nearest', cmap="RdYlGn_r")
    plt.scatter(*zip(*peaks), marker='.', color='blue')
    plt.title(songname + ' 时频谱和峰值点')
    plt.xlabel('时间')
    plt.ylabel('频率块')
    fig.savefig("plots/时频谱和峰值点 " + songname + ".png")


# 绘制songID直方图
def plot_songbins(songbins, numSongs, songnames, queryname):
    fig = plt.figure()
    ax = fig.add_subplot()
    idx = np.arange(numSongs)
    width = 0.35
    plt.bar(idx,songbins,width,color='blue',align='center')
    ax.set_ylabel('相同哈希数')
    ax.set_xticks(idx)
    ax.set_xticklabels(songnames)
    plt.title(queryname + ' 相同哈希数')
    fig.savefig("plots/" + queryname + " 相同哈希数.png")


# 绘制songID直方图
def plot_maxnums(maxnums, numSongs, songnames, queryname):
    fig = plt.figure()
    ax = fig.add_subplot()
    idx = np.arange(numSongs)
    width = 0.35
    plt.bar(idx,maxnums,width,color='blue',align='center')
    ax.set_ylabel('相同时间差最高出现次数')
    ax.set_xticks(idx)
    ax.set_xticklabels(songnames)
    plt.title(queryname + ' 相同时间差最高出现次数')
    fig.savefig("plots/" + queryname + " 相同时间差最高出现次数.png")

