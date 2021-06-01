import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import librosa
import librosa.display
import librosa.core.pitch
from scipy import signal

# do artykułu
y, fs = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))

f0 = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
times = librosa.times_like(f0)
x_f0 = np.linspace(0,len(y)/fs,len(f0)) # x do f0

# print('yin fo: ',f0)
# print('len f to\n',len(f0))

czy_filtrowac = 1
f0_filtr = []
if czy_filtrowac ==1:
    for i in range(len(f0)):
        if f0[i] > 350:
            f0_filtr.append(0)
        #if x_f0[i] > 14.8:
            #f0_filtr.append(0)
        else:
            f0_filtr.append(f0[i])


sizee = 15

plt.plot(x_f0,f0_filtr)
plt.ylabel('Częstotliwość [Hz]', size = sizee)
plt.title('Karol pięknie gra', size = sizee)
plt.xlabel('Czas [s]', size = sizee)
plt.xlim(0,14.98)
plt.xticks(size = sizee)
plt.yticks(size = sizee)





plt.show()


plt.ylabel('Częstotliwość [Hz]', size = sizee)
plt.title('Spektrogram dźwięku o F0 = 349 Hz z wykorzystaniem metody YIN', size = sizee)

plt.ylim(0,1200)
plt.xlim(0,len(y)/fs)
plt.xlabel('Czas [s]', size = sizee)
plt.xticks(size = sizee)
plt.yticks(size = sizee)

#plt.show()

