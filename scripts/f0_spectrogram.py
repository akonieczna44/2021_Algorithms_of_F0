import librosa, librosa.display
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from scipy import signal
from scipy.fftpack import fftshift


# spectrogram
def f0__spectrogram():
    y, sr = librosa.load(
        filedialog.askopenfilename(title="Wybierz plik", filetypes=(("wav mono files", ".wav"), ("all files", "*.*"))))

    f, t, Sxx = signal.spectrogram(y, sr)

    plt.pcolormesh(t, f, Sxx, shading='gouraud')
    sizee = 15
    plt.ylabel('Frequency [Hz]', size=sizee)
    plt.title('Spectrogram', size=sizee)
    plt.ylim(0, 1200)
    plt.xlim(0, len(y) / sr)
    plt.xlabel('Time [s]', size=sizee)
    plt.xticks(size=sizee)
    plt.yticks(size=sizee)
    plt.show()

    print('You have to choose the brightest frequency value from the spectrogram, this is most likely F0. ')


# for checking if sth works
# f0__spectrogram()
