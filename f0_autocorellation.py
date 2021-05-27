import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from tkinter import filedialog
from scipy.signal import correlate
from time import time

# autokorelacja
# 1. liczę funkcję autokorelacji
# 2. szukam pierwszego maksimum
# 3. obliczam f0 przy pomocy...
# -----------------------------------
# 1/T = f0
# liczba próbek = czas nagrania * fs
# czas nagrania = liczba próbek / fs
# ...
# f0 = 1 / (liczba próbek/fs) = fs/ liczba próbek
# np. dla f0 = 220.5 Hz maksymalny peak funkcji autokorelacji jest w miejscu 100.
# czyli f0 = 22050/100 = 220.5 Hz
# -----------------------------------
# wychodzi w miarę w porządku, ale trzeba to przepisać ładnie i dopisać tutaj
# przy vib1 wychodzi wszędzie inaczej lub tylko autokorelacja dobrze


def parabolic(f, x):
    """Quadratic interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.
    f is a vector and x is an index for that vector.
    Returns (vx, vy), the coordinates of the vertex of a parabola that goes
    through point x and its two neighbors.
    Example:
    Defining a vector f with a local maximum at index 3 (= 6), find local
    maximum if points 2, 3, and 4 actually defined a parabola.
    In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]
    In [4]: parabolic(f, argmax(f))
    Out[4]: (3.2142857142857144, 6.1607142857142856)
    """
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)


def freq_from_autocorr(sig, fs):
    """
    Estimate frequency using autocorrelation
    """
    # Calculate autocorrelation and throw away the negative lags
    corr = correlate(sig, sig, mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = np.diff(corr)
    start = np.nonzero(d > 0)[0][0]

    x_corr = np.linspace(0, len(corr)/fs, len(corr))
    sizee = 13
    plt.plot(x_corr, corr)
    plt.title('Funkcja autokorelacji', size = sizee)
    plt.grid()
    plt.ylabel('Amplituda', size = sizee)
    plt.xlabel('Czas [s]', size = sizee)
    plt.xticks(size = sizee)
    plt.yticks(size = sizee)

    plt.show()

    # Find the next peak after the low point (other than 0 lag)
    peak = np.argmax(corr[start:]) + start
    print('peak is ',peak)
    px, py = parabolic(corr, peak)
    return fs / px

def f0__autocorellation():

    y, fs = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))


    print('Peak ', end=' ')
    start_time = time()
    print('Autokorelacja F0 = %f Hz' % round(freq_from_autocorr(y, fs),4))
    print('Time elapsed: %.3f s\n' % (time() - start_time))

    # to do - autok.
    plt.plot(y)
    plt.title('Przebieg czasowy sygnału')
    plt.show()

f0__autocorellation()

