# analiza przejść przez zeroo
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import librosa

"""
#moje dane próbne
fs = 16000
time = 0.1

data = [-1,-2,-5,2,3,4,10,2,30,-40,-40]
ile_brakuje = int(fs*time - len(data))
print(ile_brakuje)
for i in range(ile_brakuje):
    data.append(data[-1]) #dodaje ostatni element, żeby nie było dodatkowego naliczania

print('len data to ', len(data))

plt.plot(data)
plt.show()

"""
data, fs = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))), sr=16000)


print('123')

znaki = np.sign(data)
print('znaki to ', znaki)

pochodna = np.diff(znaki)
print('pochodna to ', pochodna)

licznik = (pochodna != 0).sum()
print('licznik ', licznik)

plt.plot(data)
plt.show()


f0 = 1/licznik
f0 = licznik * fs/ len(data)/2 
#nie wiem czemu przez dwa, no ale tak rozpoznaje
print('f0 to ', f0)