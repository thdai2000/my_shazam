import numpy as np


# 找到距离目标区域的时频点
def findAdjPts(index,A,delay_time,delta_time,delta_freq):
    adjPts = []
    low_x = A[index][0]+delay_time
    high_x = low_x+delta_time
    low_y = A[index][1]-delta_freq/2
    high_y = A[index][1]+delta_freq/2
    
    for i in A:
        if ((i[0]>low_x and i[0]<high_x) and (i[1]>low_y and i[1]<high_y)):
            adjPts.append(i)
            
    return adjPts


# 创建歌曲的哈希矩阵，每行哈希的格式为：[[f1, f2, Δt], t1, songID]
def hashPeaks(A,songID,delay_time,delta_time,delta_freq):
    hashMatrix = np.zeros((len(A)*100,5))  # 限制矩阵大小，行数不超过峰值点数量的100倍
    index = 0
    numPeaks = len(A)
    for i in range(0,numPeaks):
        adjPts = findAdjPts(i,A,delay_time,delta_time,delta_freq)
        adjNum=len(adjPts)
        for j in range(0,adjNum):
            hashMatrix[index][0] = A[i][1]
            hashMatrix[index][1] = adjPts[j][1]
            hashMatrix[index][2] = adjPts[j][0]-A[i][0]
            hashMatrix[index][3] = A[i][0]
            hashMatrix[index][4] = songID
            index=index+1
    
    hashMatrix = hashMatrix[~np.all(hashMatrix==0,axis=1)]
        
    return hashMatrix


# 创建样本的哈希矩阵，每条哈希的格式为：[[f1, f2, Δt], t1, songID]
def hashSamplePeaks(A,delay_time,delta_time,delta_freq):
    hashMatrix = np.zeros((len(A)*100,4))
    index = 0
    numPeaks = len(A)
    for i in range(0,numPeaks):
        adjPts = findAdjPts(i,A,delay_time,delta_time,delta_freq)
        adjNum = len(adjPts)
        for j in range(0,adjNum):
            hashMatrix[index][0] = A[i][1]
            hashMatrix[index][1] = adjPts[j][1]
            hashMatrix[index][2] = adjPts[j][0]-A[i][0]
            hashMatrix[index][3] = A[i][0]
            index=index+1

    hashMatrix = hashMatrix[~np.all(hashMatrix==0,axis=1)]
        
    return hashMatrix


# 对样本每一条哈希，在哈希库中找到与其匹配的哈希，若找到，则记录时间对(t1, t1')和songID
def findTimePairs(hash_database,sample_hash,deltaTime,deltaFreq):
    timePairs = []
    for i in sample_hash:
        for j in hash_database:
            if(i[0] > (j[0]-deltaFreq) and i[0] < (j[0] + deltaFreq)):
                if(i[1] > (j[1]-deltaFreq) and i[1] < (j[1] + deltaFreq)):
                    if(i[2] > (j[2]-deltaTime) and i[2] < (j[2] + deltaTime)):
                        timePairs.append((j[3],i[3],j[4]))
                    else:
                        continue
                else:
                    continue
            else:
                continue

    return timePairs
