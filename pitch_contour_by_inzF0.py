import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from tkinter import filedialog
from scipy.fftpack import fft
import wave

print('start')

y, sr = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))

# ---------------------------------------------------------- dane nagrania
x = np.linspace(0, len(y)/sr, num=len(y))
print('x len to', len(x))
print('x to ', x)
print('sr to ', sr)
print('ilość próbek pliku to ', len(y))


# ---------------------------------------------------------- samo fft z funkcji
fft_signal = fft(y)
n_fft = len(fft_signal)

# ---------------------------------------------------------- prawidłowe x,y fft
xf = np.linspace(0.0, sr / 2.0, n_fft // 2)
fft_y = 2.0 / n_fft * np.abs(fft_signal[0:n_fft // 2])

# ---------------------------------------------------------- filtrowanie fft i pomocnicza linia granicy amplitudy

prog_amp = 0.015 #zmienna wartość w zależności od rodzaju nagrania
prog_min = 0.005 #poniżej tej wartości w widmie zeruję

line = []
for i in range(len(xf)):
    line.append(prog_amp)
# print('line to ', line)


fft_y_filtr = []
for i in range(len(fft_y)):
    if round(fft_y[i],2) < prog_min:
        fft_y_filtr.append(0)
    else:
        fft_y_filtr.append(fft_y[i])


#plt.show()

plt.subplot(2,1,1)
plt.plot(xf, fft_y)
plt.plot(line)
plt.title('pierwsze DOBRE fft')
plt.xlim(0,2000)
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')

plt.subplot(2,1,2)
plt.plot(xf, fft_y_filtr)
plt.plot(line)
#plt.title('filtr fft')
plt.xlim(0,2000)
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
#plt.plot(x,y)
#plt.title('audio')
plt.show()


#############

############ znajdowanie f0 - metoda z inżynierki
def get_fft(fft_y_filtr):


    def prazki_widma (widmo, prog, rozmiar_okna, fs):
        ponad = (widmo >= prog).astype(
            np.int)  # kiedy będzie powyżej, to zmienna będzie True od razu przekonwertowana na 1
        pochodna = np.diff(ponad)  # kiedy będzie zmiana z 0 na 1, to pochodna się zmieni i udowodni wykrycie prążka
        
        xf_def = np.linspace(0.0, 22050 / 2.0, len(pochodna))
        
        print('len pochodna ',len(pochodna))
        print('len xff', len(xf_def))
        
        plt.subplot(2,1,1)
        plt.plot(pochodna)
        plt.title('bez xf')

        plt.subplot(2,1,2)
        plt.plot(xf_def,pochodna)
        plt.title('z xf')
        plt.show()

        
        # to wskazuje tylko na miejsce w liście "pochodna". trzeba uwzględnić jednak x jako linspace, 
        # żeby wskazywał gdzie zmienia się pochodna przy konkretnej wartości z- Hz
        """
        poczatki = np.where(pochodna == 1)[0] + 1
        konce = np.where(pochodna == -1)[0] + 1

        #print('początki to ',poczatki_stare)
        #print('konce to ', konce_stare)
        """
        poczatki_where = np.where(pochodna == 1)[0] + 1
        konce_where = np.where(pochodna == -1)[0] + 1
        # może z tego trzeba zrobić ładną listę forem....
        poczatki = xf_def[poczatki_where]
        konce = xf_def[konce_where]

        # przerabianie otrzymanych wartości na int..
        poczatki_int = []
        konce_int = []
        for i in range(len(poczatki)):
            print('poczatki przed ',poczatki[i])
            poczatki_int.append(int(poczatki[i]))
            
            print('poczatki po ',poczatki_int[i])

        for i in range(len(konce)):
            konce_int.append(int(konce[i]))

        poczatki = poczatki_int
        konce = konce_int

        prazki = []
        print('początki NOWE to ',poczatki)
        print('konce NOWE to ', konce)


        #print('nowe xff początki z uzwględnieniem dobrym ', xf_def[211], ' ', xf_def[422], ' ', xf_def[428])
        
        for poczatek, koniec in zip(poczatki, konce):
            p = np.argmax(widmo[poczatek:koniec]) + poczatek
            argmax = np.argmax(widmo[poczatek:koniec])
            print('arg max to ',argmax)
            print('poczatek to ', poczatek)
            #print('p to ',p, type(p))
            a, b, c = widmo[p - 1:p + 2]
            k = 0.5 * (a - c) / (a - 2 * b + c)
            prazki.append((p + k) * fs / rozmiar_okna*2) # dodane *2
            print('prążki wychodzące z funkcji to', prazki)
        return prazki

    prazki = prazki_widma(fft_y, prog_amp, 2048, 1024)
    numer_prazka = 1
    for p in prazki:
        print('prążek{} = {}, współczynnik = {}'.format(numer_prazka, round(p,3), round(p / prazki[0],1)))
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
    print('odleglosci to ', odleglosci)


    print('Częstotliwość zaśpiewanego dźwięku to: {} Hz'.format(voice_fft))

    return voice_fft

fffttt = get_fft(fft_y)
print(fffttt)

"""
S = np.abs(librosa.stft(y))
S_left = librosa.stft(y, center=False)
D_short = librosa.stft(y, hop_length=64)

fig, ax = plt.subplots()

img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),y_axis='log', x_axis='time', ax=ax)

ax.set_title('Power spectrogram')

fig.colorbar(img)
"""