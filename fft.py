import numpy as np
import librosa


def stft(signal, windowsize, windowshift):
    S_scale = librosa.stft(signal, n_fft=windowsize, hop_length=windowshift)
    Y_scale = np.abs(S_scale) ** 2
    Y_log_scale = librosa.power_to_db(Y_scale)

    return Y_log_scale
