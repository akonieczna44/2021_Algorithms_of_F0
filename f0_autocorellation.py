import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from tkinter import filedialog
from scipy.signal import correlate
from time import time


# Autocorrelation
# 1. Compute the autocorrelation function
# 2. Searching for the first maximum
# 3. Calculate f0 using...
# -----------------------------------
# 1/T = f0
# number of samples = recording time * fs
# recording time = number of samples / fs
# ...
# f0 = 1 / (number of samples/fs) = fs/ number of samples
# e.g. for f0 = 220.5 Hz the maximum peak of the autocorrelation function is at the 100th location
# so f0 = 22050/100 = 220.5 Hz
# -----------------------------------
# Comes out pretty much right
# The algorithm works best of the others if there is vibrato articulation in the recording


# Some function is from
# https://github.com/kwinkunks/notebooks/blob/master/parabolic.py

def parabolic(f, x):
    xv = 1 / 2. * (f[x - 1] - f[x + 1]) / (f[x - 1] - 2 * f[x] + f[x + 1]) + x
    yv = f[x] - 1 / 4. * (f[x - 1] - f[x + 1]) * (xv - x)
    return (xv, yv)


def freq_from_autocorr(sig, fs):
    # Estimate frequency using autocorrelation
    # Calculate autocorrelation and throw away the negative lags
    corr = correlate(sig, sig, mode='full')
    corr = corr[len(corr) // 2:]

    # Find the first low point
    d = np.diff(corr)
    start = np.nonzero(d > 0)[0][0]

    # Optional plot
    # x_corr = np.linspace(0, len(corr)/fs, len(corr))
    # sizee = 13
    # plt.plot(x_corr, corr)
    # plt.title('', size = sizee)
    # plt.grid()
    # plt.ylabel('Amplitude', size = sizee)
    # plt.xlabel('Time [s]', size = sizee)
    # plt.xticks(size = sizee)
    # plt.yticks(size = sizee)
    # plt.show()

    # Find the next peak after the low point (other than 0 lag)
    peak = np.argmax(corr[start:]) + start
    # print('Peak is ',peak)
    px, py = parabolic(corr, peak)
    return fs / px


def f0__autocorellation():
    y, fs = librosa.load(
        filedialog.askopenfilename(title="Wybierz plik", filetypes=(("wav mono files", ".wav"), ("all files", "*.*"))))

    print('Autokorelacja F0 = %f Hz' % round(freq_from_autocorr(y, fs), 4))
    # start_time = time()
    # print('Time elapsed: %.3f s\n' % (time() - start_time))

    # to do - autok.
    sizee = 13
    plt.plot(y)
    plt.title('Time waveform of a sound', size=sizee)
    plt.grid()
    plt.ylabel('Amplitude', size=sizee)
    plt.xlabel('Time [s]', size=sizee)
    plt.xticks(size=sizee)
    plt.yticks(size=sizee)
    plt.show()


# for checking if sth works
# f0__autocorellation()
