import librosa, librosa.display
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from scipy import signal
from scipy.fftpack import fftshift

# spectro - raczej wyświetlanie niż liczenie chyba

def f0__spectrogram():

    y, sr = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))

    f, t, Sxx = signal.spectrogram(y, sr)

    plt.pcolormesh(t, f, Sxx) # shading='gouraud'

    plt.ylabel('Frequency [Hz]')
    plt.ylim(0,1200)
    plt.xlim(0,len(y)/sr)
    plt.xlabel('Time [sec]')
    plt.show()

f0__spectrogram()
"""
librosa.feature.melspectrogram(y=y, sr=sr)


S = np.abs(librosa.stft(y))
S_left = librosa.stft(y, center=False)
D_short = librosa.stft(y, hop_length=64)

fig, ax = plt.subplots()
S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time',
y_axis='mel', sr=sr,
fmax=8000, ax=ax)
plt.colorbar(img, ax=ax)

#fig.colorbar(img, ax=ax, format='%+2.0f dB')

ax.set(title='Mel-frequency spectrogram')
"""
