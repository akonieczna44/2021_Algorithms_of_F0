import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from tkinter import filedialog
from scipy.fftpack import fft

# metoda detekcji f0 polegająca na przypisaniu jej wartości pierwszej odległości między harmonicznymi
# 1. widmo fft i jego subtelna filtracja małych wartości
# 2. obliczenie średniej prążków (znajdujących się w bliskim sąsiedztwie)
# 3. obliczenie odległości i przypisanie f0

def f0__pitch_contour_by_inz():
        
    # ---------------------------------------------------------- 1.

    y, sr = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))
    x = np.linspace(0, len(y)/sr, num=len(y))

    # ---------------------------------------------------------- samo fft z funkcji, biblioteka scipy
    fft_signal = fft(y)
    fft_n = len(fft_signal)

    # ---------------------------------------------------------- prawidłowe x,y fft
    fft_x = np.linspace(0.0, sr / 2.0, fft_n // 2)
    fft_y = 2.0 / fft_n * np.abs(fft_signal[0:fft_n // 2])

    # ---------------------------------------------------------- filtrowanie fft i pomocnicza linia granicy amplitudy

    prog_amp = 0.0071 # zmienna wartość w zależności od rodzaju nagrania i wartości amplitudy
    prog_min = 0.003 # poniżej tej wartości w widmie zeruję

    line = []
    for i in range(len(fft_x)):
        line.append(prog_amp)

    fft_y_filtr = []
    for i in range(len(fft_y)):
        if fft_y[i] < prog_min:
            fft_y_filtr.append(0)
        else:
            fft_y_filtr.append(fft_y[i])

    plt.subplot(2,1,1)
    plt.plot(fft_x, fft_y)
    plt.plot(line)
    plt.title('FFT signal')
    plt.xlim(0,2000)
    plt.ylabel('Amplituda')
    plt.xlabel('Częstotliwość [Hz]')

    plt.subplot(2,1,2)
    plt.plot(fft_x, fft_y_filtr)
    plt.plot(line)
    plt.title('After')
    plt.xlim(0,2000)
    plt.ylabel('Amplituda')
    plt.xlabel('Częstotliwość [Hz]')
    plt.show()

    # ---------------------------------------------------------- 2. znajdowanie f0 - metoda z inżynierki

    def prazki_widma (widmo, prog, rozmiar_okna, fs):
        ponad = (widmo >= prog).astype(
            np.int)  # kiedy będzie powyżej, to zmienna będzie True przekonwertowana na 1
        pochodna = np.diff(ponad)  # kiedy będzie zmiana z 0 na 1, to pochodna się zmieni i udowodni wykrycie prążka
        fft_x_def = np.linspace(0.0, 22050 / 2.0, len(pochodna))
        
        plt.subplot(2,1,1)
        plt.plot(pochodna)
        plt.title('bez fft_x')

        plt.subplot(2,1,2)
        plt.plot(fft_x_def,pochodna)
        plt.title('z fft_x')
        # plt.show()
        """
        # to wskazuje tylko na miejsce w liście "pochodna". trzeba uwzględnić jednak x jako linspace, 
        # żeby wskazywał gdzie zmienia się pochodna przy konkretnej wartości z- Hz
        poczatki = np.where(pochodna == 1)[0] + 1
        konce = np.where(pochodna == -1)[0] + 1

        #print('początki to ',poczatki_stare)
        #print('konce to ', konce_stare)
        """
        # miejsca zmiany pochodnej, ale w liście pochodna
        poczatki_where = np.where(pochodna == 1)[0] + 1
        konce_where = np.where(pochodna == -1)[0] + 1
        
        # miejsca zmiany pochodnej, ALE w dziedzinie częstotliwości fft_x
        # wyjście to wartość w Hz z wektora fft_x
        poczatki = fft_x_def[poczatki_where]
        konce = fft_x_def[konce_where]

        # przerabianie otrzymanych wartości na int..
        poczatki_int = []
        konce_int = []
        for i in range(len(poczatki)):
            poczatki_int.append(int(poczatki[i]))

        for i in range(len(konce)):
            konce_int.append(int(konce[i]))

        poczatki = poczatki_int
        konce = konce_int

        prazki = []
        #print('początki to ',poczatki)
        #print('konce to ', konce)
        # ---------------------------------------------------------- 3. uśrednianie prążków
        for poczatek, koniec in zip(poczatki, konce):
            p = np.argmax(widmo[poczatek:koniec]) + poczatek
            a, b, c = widmo[p - 1:p + 2]
            k = 0.5 * (a - c) / (a - 2 * b + c)
            prazki.append((p + k) * fs / rozmiar_okna*2) # dodane *2
        return prazki

    prazki = prazki_widma(fft_y, prog_amp, 2048, 1024)
    numer_prazka = 1

    for p in prazki:
        print('prążek{} = {}, współczynnik = {}'.format(numer_prazka, round(p,3), round(p / prazki[0],1)))
        numer_prazka = numer_prazka + 1

    # ---------------------------------------------------------- 3. harmoniczne
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
            odleglosci.append(round(harmoniczne[licznik + 1] - harmoniczne[licznik],2))
            licznik += 1

    # ---------------------------------------------------------- 3. przypisanie f0
    voice_fft = round(odleglosci[0], 3)
    print('\nOdleglosci to ', odleglosci)
    print('\nCzęstotliwość zaśpiewanego dźwięku to: {} Hz\n'.format(voice_fft))

print('koniec')


f0__pitch_contour_by_inz()