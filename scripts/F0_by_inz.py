import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from tkinter import filedialog
from scipy.fftpack import fft


# Method of detecting F0 that was created in an engineering thesis that involves...
# 1. Making a frequency spectrum
# 2. Calculating the harmonic bars and filtering them above a fixed amplitude value
# 3. Averaging the values of the peaks # 4. calculating the distance between them
# 4. Calculating the distance between them
# 5. Assign the value f0 to the first distance between harmonics

def f0__pitch_contour_by_inz():
    # ---------------------------------------------------------- 1.

    y, sr = librosa.load(
        filedialog.askopenfilename(title="Wybierz plik", filetypes=(("wav mono files", ".wav"), ("all files", "*.*"))))
    # x = np.linspace(0, len(y)/sr, num=len(y))

    # ---------------------------------------------------------- only fft from function, library scipy
    fft_signal = fft(y)
    fft_n = len(fft_signal)

    # ---------------------------------------------------------- right x,y fft
    fft_x = np.linspace(0.0, sr / 2.0, fft_n // 2)
    fft_y = 2.0 / fft_n * np.abs(fft_signal[0:fft_n // 2])

    # ---------------------------------------------------------- fft filtering and additional amplitude limit line

    prog_amp = 0.008  # variable value depending on type of recording and amplitude value
    prog_min = 0.005  # below this value in the spectrum I put a zero

    line = []
    for i in range(len(fft_x)):
        line.append(prog_amp)

    fft_y_filtr = []
    for i in range(len(fft_y)):
        if fft_y[i] < prog_min:
            fft_y_filtr.append(0)
        else:
            fft_y_filtr.append(fft_y[i])

    plt.subplot(2, 1, 1)
    plt.plot(fft_x, fft_y)
    plt.plot(line)
    plt.title('FFT signal')
    plt.xlim(0, 2000)
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency [Hz]')

    plt.subplot(2, 1, 2)
    plt.plot(fft_x, fft_y_filtr)
    plt.plot(line)
    plt.title('After filtering the spectral values')
    plt.xlim(0, 2000)
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency  [Hz]')
    plt.show()

    # ------------------ 2. Calculating the harmonic bars and filtering them above a fixed amplitude value

    def prazki_widma(widmo, prog, rozmiar_okna, fs):
        ponad = (widmo >= prog).astype(
            np.int)  # when above, the variable will be True converted to 1
        pochodna = np.diff(
            ponad)  # when there is a change from 0 to 1, the derivative will change and prove the detection of peak
        fft_x_def = np.linspace(0.0, 22050 / 2.0, len(pochodna))

        # locations of the derivative change, but in the list the derivative
        poczatki_where = np.where(pochodna == 1)[0] + 1
        konce_where = np.where(pochodna == -1)[0] + 1

        # where the derivative changes, BUT in the frequency domain fft_x
        # output is the value in Hz from the fft_x vector
        poczatki = fft_x_def[poczatki_where]
        konce = fft_x_def[konce_where]

        # converting the received values into int...
        poczatki_int = []
        konce_int = []
        for i in range(len(poczatki)):
            poczatki_int.append(int(poczatki[i]))

        for i in range(len(konce)):
            konce_int.append(int(konce[i]))

        poczatki = poczatki_int
        konce = konce_int
        prazki = []

        # ---------------------------------------------------------- 3. Averaging the values of the peaks
        for poczatek, koniec in zip(poczatki, konce):
            p = np.argmax(widmo[poczatek:koniec]) + poczatek
            a, b, c = widmo[p - 1:p + 2]
            k = 0.5 * (a - c) / (a - 2 * b + c)
            prazki.append((p + k) * fs / rozmiar_okna * 2)  # dodane *2
        return prazki

    prazki = prazki_widma(fft_y, prog_amp, 2048, 1024)
    numer_prazka = 1

    # additional print function
    # controlling whether there are harmonics
    # for p in prazki:
    #     print('prążek{} = {}, współczynnik = {}'.format(numer_prazka, round(p,3), round(p / prazki[0],1)))
    #     numer_prazka = numer_prazka + 1

    # ---------------------------------------------- 4. Harmonics peaks, and calculating the distance between them
    harmoniczne = []
    harmoniczne.append(prazki[0])
    ilosc_pomiarow = 1

    for p in prazki[1:]:
        if (harmoniczne[-1] / p) > 0.9:
            harmoniczne[-1] = (harmoniczne[-1] * ilosc_pomiarow + p) / (ilosc_pomiarow + 1)
            ilosc_pomiarow += 1
        else:
            harmoniczne.append(p)
            ilosc_pomiarow = 1

    licznik = 0
    odleglosci = []

    for har in range(len(harmoniczne) - 1):
        if licznik == len(harmoniczne):
            break

        elif licznik < len(harmoniczne):
            odleglosci.append(round(harmoniczne[licznik + 1] - harmoniczne[licznik], 2))
            licznik += 1

    # ---------------------------------------------------------- 3. przypisanie f0
    voice_fft = round(odleglosci[0], 3)
    print('\nThe distance is ', odleglosci)
    print('\nThe frequency of the sung sound is: {} Hz\n'.format(voice_fft))


# for checking if sth works
# f0__pitch_contour_by_inz()
