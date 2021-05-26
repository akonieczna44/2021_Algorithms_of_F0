import librosa
import matplotlib.pyplot as plt
from tkinter import filedialog
from scipy import signal


def f0__welch():
    y, sr = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))))

    f, Pwelch_spec = signal.welch(y, sr, scaling='spectrum')

    plt.semilogy(f, Pwelch_spec)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD')
    plt.title('Power Welch')
    plt.grid()
    plt.show()