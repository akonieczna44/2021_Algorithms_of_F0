import librosa
import matplotlib.pyplot as plt
from tkinter import filedialog
from scipy import signal


def f0__welch():
    y, sr = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))

    f, Pwelch_spec = signal.welch(y, sr, scaling='spectrum')

    sizee = 14

    plt.semilogy(f, Pwelch_spec)
    plt.xlabel('Częstotliwość [Hz]',size = sizee)
    plt.ylabel('PSD',size = sizee)
    plt.title('Moc sygnału na dane pasmo częstotliwości',size = sizee)
    plt.grid()
    plt.xticks(size = sizee)
    plt.yticks(size = sizee)
    plt.show()

f0__welch()

"""
# wyniki dla sinusa





"""