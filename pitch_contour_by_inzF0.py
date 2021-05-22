import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from tkinter import filedialog
from scipy.fftpack import fft
import wave

print('start')

y, sr = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))


"""
adres = "C:\\Users\\konie\\OneDrive\\Pulpit\\nagrania\\do programu\\piano\\69.wav"
wf = wave.open(adres, 'rb')
signal = wf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
#print('wf n ', len(signal), 'y len', len(y))
a = 3
print('n frames', wf.getnframes())

print('sr - sampling rate.. ', wf.getframerate())
sr = wf.getframerate()


print('len signal',len(signal))
########### ========================================
#y = signal
"""

x = np.linspace(0, len(y)/sr, num=len(y))
print('x len to', len(x))
print('x to ', x)
print('sr to ', sr)
print('ilość próbek pliku to ', len(y))


######### samo fft
fft_signal = fft(y)
n_fft = len(fft_signal)


xf = np.linspace(0.0, sr / 2.0, n_fft // 2)
fft_y = 2.0 / n_fft * np.abs(fft_signal[0:n_fft // 2])

# pomocnicza linia granicy amplitudy
line = []
for i in range(len(xf)):
    line.append(0.01)
# print('line to ', line)

plt.subplot(2,1,1)
plt.plot(xf, fft_y)
plt.plot(line)
plt.title('pierwsze DOBRE fft')
plt.xlim(0,2000)
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
#plt.show()


plt.subplot(2,1,2)
plt.plot(x,y)
plt.title('audio')
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

    prazki = prazki_widma(fft_y, 0.01, 2048, 1024)
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