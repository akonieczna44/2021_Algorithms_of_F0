import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import librosa

# analiza przejść przez zero
# trochę moja, trochę nie
# trzeba sobie wybrać fragment sygnału, żeby to miało jakąś rację bytu..

def f0__zero_cross():

    y, fs = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))

    # wybór fragmentu
    start = 5000
    stop = start + 5000

    # klasycznie pomocnicza linia
    line = []
    for i in range(len(y)):
        if stop > i > start:
            line.append(0.1)
        else:
            line.append(0)
    
    y_part = y[start:stop]
    
    plt.subplot(2,1,1)
    plt.plot(y)
    plt.plot(line)
    plt.title('zobacz, które próbki')

    plt.subplot(2,1,2)
    plt.plot(y_part)
    plt.title('badany fragment')
    plt.show()

    def zero_cross(y):
        indices = np.nonzero((y[1:] >= 0) & (y[:-1] < 0))[0]

        # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
        # crossings = indices

        # More accurate, using linear interpolation to find intersample
        # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
        crossings = [i - y[i] / (y[i+1] - y[i]) for i in indices]

        # Some other interpolation based on neighboring points might be better.
        # Spline, cubic, whatever

        f = round(fs / np.mean(np.diff(crossings)),2)

        return f

    f0_all = zero_cross(y)
    f0_part = zero_cross(y[start:stop])
    print('f0 z całego nagrania: ',f0_all, 'Hz')
    print('f0 z fragmentu nagrania: ',f0_part, 'Hz\n')

# f0__zero_cross()





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

print(data[2:7])
"""

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
# nie wiem czemu przez dwa, no ale tak rozpoznaje
print('f0 to ', f0)
"""