# wykresy na ładnie
import librosa
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from scipy.fftpack import fft

# rozmiar font
sizee = 13

y, fs = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))
x = np.linspace(0,  len(y)/fs, len(y))


plt.plot(x, y)
#plt.plot(line)
plt.title('Przebieg czasowy dźwięku pianina', size = sizee)
plt.grid()
plt.ylabel('Amplituda', size = sizee)
plt.xlabel('Czas [s]', size = sizee)
plt.xticks(size = sizee)
plt.yticks(size = sizee)
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


plt.plot(fft_x, fft_y)
#plt.plot(line)
#plt.title('Widmo dźwięku pianina ze składową F0 = 220 Hz',size = 15)
plt.title('Widmo dźwięku woklanego ze składową F0 = 200 Hz',size = 15)
plt.xlim(0,2000)
plt.xticks(size = sizee)
plt.yticks(size = sizee)
# plt.grid()
plt.ylabel('Amplituda',size = sizee)
plt.xlabel('Częstotliwość [Hz]',size = sizee)
plt.show()


"""
plt.title('Amplituda')
plt.xlabel('Częstotliwość [Hz]')
plt.show()
"""