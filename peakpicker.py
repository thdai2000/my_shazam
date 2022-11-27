import numpy as np


# 确定峰值点的最低要求幅值，这里为不低于第percentile百分位数
# 这里的S是array，与频谱图是上下翻转关系
def find_thres(S, percentile, base):
    window = S[base:S.shape[0], 0:S.shape[1]]
    threshold = np.percentile(window, percentile)

    return threshold


# 选择峰值点，这里的S是array，与频谱图是上下翻转关系
def peak_pick(S, f_dim1, t_dim1, f_dim2, t_dim2, threshold, base):
    a = S.shape[0]  # 频率轴长度
    b = S.shape[1]  # 时间轴长度

    peaks = []
    t_coords = []
    f_coords = []

    # 生成窗口，进行全频谱图的扫描
    for i in range(base, a, f_dim1):
        for j in range(0, b, t_dim1):
            if i + f_dim1 < a and j + t_dim1 < b:
                window = S[i:i+t_dim1, j:j+f_dim1]
            elif i + f_dim1 < a and j + t_dim1 >= b:
                window = S[i:i+t_dim1, j:b]
            elif i + f_dim1 >= a and j + t_dim1 < b:
                window = S[i:a, j:j+f_dim1]
            else:
                window = S[i:a, j:b]

            # 检查该窗口的最大值是否高于幅值的最低阈值
            # amax = np.amax(window)
            if np.amax(window) >= threshold:
                row, col = np.unravel_index(np.argmax(window), window.shape)
                f_coords.append(i+row)
                t_coords.append(j+col)

    # 检查所选时频点是否是局部极大值
    for k in range(0, len(f_coords)):
        fmin = f_coords[k] - f_dim2
        fmax = f_coords[k] + f_dim2
        tmin = t_coords[k] - t_dim2
        tmax = t_coords[k] + t_dim2
        if fmin < base:
            fmin = base
        if fmax > a:
            fmax = a
        if tmin < 0:
            tmin = 0
        if tmax > b:
            tmax = b
        window = S[fmin:fmax, tmin:tmax]  # 以所选时频点为中心的一个窗口

        if not window.size:
            continue

        # 将不是局部极大值的点的横纵坐标置为-1
        if S[f_coords[k], t_coords[k]] < np.amax(window):
            f_coords[k] = -1
            f_coords[k] = -1

    # 删除不是局部极大值的点
    f_coords[:] = (value for value in f_coords if value != -1)
    t_coords[:] = (value for value in t_coords if value != -1)

    # 按[t1, f1, S(t1, f1)]格式记录峰值点
    for x in range(0, len(f_coords)):
        peaks.append((t_coords[x], f_coords[x], S[f_coords[x], t_coords[x]]))

    return peaks


# 通过定义高频区和低频区的不同阈值，实现两个目的：1.峰值点分布的均匀性 2.进一步删减峰值点
def reduce_peaks(peaks, fftsize, high_peak_threshold, low_peak_threshold):
    low_peaks = []
    high_peaks = []

    for item in peaks:
        if(item[1]>(fftsize/4)):
            high_peaks.append(item)
        else:
            low_peaks.append(item)
    
    # 基于不同的阈值，删减峰值点
    reduced_peaks = []
    for item in peaks:
        if(item[1] > (fftsize/4)):
            if(item[2] > np.percentile(high_peaks, high_peak_threshold, axis=0)[2]):
                reduced_peaks.append(item)
            else:
                continue
        else:
            if(item[2]>np.percentile(low_peaks, low_peak_threshold, axis=0)[2]):
                reduced_peaks.append(item)
            else:
                continue

    return reduced_peaks
