# wykresy na ładnie
import librosa
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from scipy.fftpack import fft


y, fs = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))
x = np.linspace(0,  len(y)/fs, len(y))


plt.plot(x, y)
#plt.plot(line)
plt.title('Przebieg czasowy dźwięku')
plt.grid()
plt.ylabel('Amplituda')
plt.xlabel('Czas [s]')
plt.show()


# ------------------------------------------------------------------------------- FFT

fft_signal = fft(y)
fft_n = len(fft_signal)

# ---------------------------------------------------------- prawidłowe x,y fft
fft_x = np.linspace(0.0, fs / 2.0, fft_n // 2)
fft_y = 2.0 / fft_n * np.abs(fft_signal[0:fft_n // 2])

# ---------------------------------------------------------- filtrowanie fft i pomocnicza linia granicy amplitudy

prog_amp = 0.01 # zmienna wartość w zależności od rodzaju nagrania i wartości amplitudy
prog_min = 0.005 # poniżej tej wartości w widmie zeruję

line = []
for i in range(len(fft_x)):
    line.append(prog_amp)

fft_y_filtr = []
for i in range(len(fft_y)):
    if fft_y[i] < prog_min:
        fft_y_filtr.append(0)
    else:
        fft_y_filtr.append(fft_y[i])

#plt.subplot(2,1,1)
plt.plot(fft_x, fft_y)
plt.plot(line)
plt.title('FFT signal')
plt.xlim(0,2000)
plt.ylabel('Amplituda')
plt.xlabel('Częstotliwość [Hz]')
plt.show()


"""
plt.title('Amplituda')
plt.xlabel('Częstotliwość [Hz]')
plt.show()
"""