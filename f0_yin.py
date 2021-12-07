import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import librosa
import librosa.display
import librosa.core.pitch
from scipy import signal


# YIN is an algorithm inspired by the autocorrelation function

def fun__YIN():
    y, fs = librosa.load(
        filedialog.askopenfilename(title="Wybierz plik", filetypes=(("wav mono files", ".wav"), ("all files", "*.*"))))

    f0 = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    # times = librosa.times_like(f0)

    # values from this vector could be averaged, but for now the maximum value from them is chosen
    # additionally, it is worth to make here an octave error handling
    print('f0 from YIN: ', max((f0)))

    x_f0 = np.linspace(0, len(y) / fs, len(f0))  # x to f0
    sizee = 15

    f, t, Sxx = signal.spectrogram(y, fs)
    plt.pcolormesh(t, f, Sxx, shading='gouraud')
    plt.plot(x_f0, f0, color='red', label='F0')  # this line indicates the f0 waveform during the recording

    plt.ylabel('Frequency [Hz]', size=sizee)
    plt.title('Spectrogram with YIN', size=sizee)

    plt.ylim(0, 1200)
    plt.xlim(0, len(y) / fs)
    plt.xlabel('Time [s]', size=sizee)
    plt.xticks(size=sizee)
    plt.yticks(size=sizee)
    plt.show()

# for checking if sth works
# fun__YIN()
