import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import librosa
import librosa.display
import librosa.core.pitch

# yin działa po najnowszej aktualizacji librosy ;)))
y, fs = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))
print('fs ', fs)

print(librosa.__version__)

f0 = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
times = librosa.times_like(f0)

print('yin fo: ',f0)
print('przeszło\n')

D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
fig, ax = plt.subplots()
img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
ax.set(title='pYIN fundamental frequency estimation')
fig.colorbar(img, ax=ax, format="%+2.f dB")
ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
ax.legend(loc='upper right')
plt.show()
print('poszło')
