import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import librosa
from numpy.core.function_base import linspace


# Time domain function
# Zero crossing analysis
# You have to be careful what passage you take

def f0__zero_cross():
    y, fs = librosa.load(
        filedialog.askopenfilename(title="Wybierz plik", filetypes=(("wav mono files", ".wav"), ("all files", "*.*"))))

    x = linspace(0, len(y) / fs, len(y))
    # choose fragment of file to analyse!
    # 14000, 18000, 24000 for presentation
    start = 12000
    stop = start + 2205  # + 10 ms

    # additional line
    line = []
    line_y = round(max(y), 3)

    for i in range(len(y)):
        if stop > i > start:
            line.append(line_y)
        else:
            line.append(0)
    sizee = 13
    y_part = y[start:stop]

    plt.subplot(2, 1, 1)
    plt.plot(x, y)
    plt.plot(x, line)
    plt.title('Time waveform of a sound', size=sizee)
    plt.grid()
    plt.ylabel('Amplitude', size=sizee)
    # plt.xlabel('Czas [s]', size = sizee)
    plt.xticks(size=sizee)
    plt.yticks(size=sizee)

    plt.subplot(2, 1, 2)
    plt.plot(x[start:stop], y_part)
    plt.title('Fragment of time waveform', size=sizee)
    plt.xlabel('Time [s]', size=sizee)
    plt.xticks(size=sizee)
    plt.yticks(size=sizee)
    plt.xlim(x[start], x[stop])
    plt.grid()
    plt.show()

    def zero_cross(y):
        indices = np.nonzero((y[1:] >= 0) & (y[:-1] < 0))[0]
        crossings = [i - y[i] / (y[i + 1] - y[i]) for i in indices]
        f = round(fs / np.mean(np.diff(crossings)), 2)

        return f

    f0_all = zero_cross(y)
    f0_part = zero_cross(y[start:stop])
    print('F0 (signal): ', f0_all, 'Hz')
    print('F0 (part of signal): ', f0_part, 'Hz\n')

# for checking if sth works
# f0__zero_cross()
