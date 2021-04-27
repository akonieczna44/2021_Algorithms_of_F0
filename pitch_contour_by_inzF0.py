import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from tkinter import filedialog
from scipy.fftpack import fft

y, sr = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))), sr=16000)

a = 3
print(a)

######### samo fft
fft_signal = fft(y)
n_fft = len(fft_signal)

xf = np.linspace(0.0, sr / 2.0, n_fft // 2)
fft_y = 2.0 / n_fft * np.abs(fft_signal[0:n_fft // 2])
plt.plot(fft_y)
plt.show()

#############

############ znajdowanie f0 - metoda z inżynierki
def get_fft(fft_y):


    def prazki_widma (widmo, prog, rozmiar_okna, fs):
        ponad = (widmo >= prog).astype(
            np.int)  # kiedy będzie powyżej, to zmienna będzie True od razu przekonwertowana na 1
        pochodna = np.diff(ponad)  # kiedy będzie zmiana z 0 na 1, to pochodna się zmieni i udowodni wykrycie prążka
        poczatki = np.where(pochodna == 1)[0] + 1
        konce = np.where(pochodna == -1)[0] + 1
        prazki = []
        for poczatek, koniec in zip(poczatki, konce):
            p = np.argmax(widmo[poczatek:koniec]) + poczatek
            a, b, c = widmo[p - 1:p + 2]
            k = 0.5 * (a - c) / (a - 2 * b + c)
            prazki.append((p + k) * fs / rozmiar_okna)
        return prazki

    prazki = prazki_widma(fft_y, 0.02, 2048, 1024)
    numer_prazka = 1
    for p in prazki:
        numer_prazka = numer_prazka + 1

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
            odleglosci.append(harmoniczne[licznik + 1] - harmoniczne[licznik])
            licznik += 1

    voice_fft = round(odleglosci[0], 3)
    print('Częstotliwość zaśpiewanego dźwięku to: {} Hz'.format(voice_fft))

    return voice_fft

fffttt = get_fft(fft_y)
print(fffttt)
