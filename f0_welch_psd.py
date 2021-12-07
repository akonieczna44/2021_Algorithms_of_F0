import librosa
import matplotlib.pyplot as plt
from tkinter import filedialog
from scipy import signal


# This function is probably for visualize what band to look for F0 in, not where its specific value is
# Some function from matplotlib library

def f0__welch():
    y, sr = librosa.load(
        filedialog.askopenfilename(title="Wybierz plik", filetypes=(("wav mono files", ".wav"), ("all files", "*.*"))))

    f, Pwelch_spec = signal.welch(y, sr, scaling='spectrum')

    sizee = 14

    plt.semilogy(f, Pwelch_spec)
    plt.xlabel('Frequency [Hz]', size=sizee)
    plt.ylabel('PSD', size=sizee)
    plt.title('Power of the signal for a given frequency band', size=sizee)
    plt.grid()
    plt.xticks(size=sizee)
    plt.yticks(size=sizee)
    plt.show()


# for checking if sth works
# f0__welch()
