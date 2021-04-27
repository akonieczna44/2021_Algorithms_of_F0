impoort librosa
import numpy as np
impoort matplotlib.pyplot as plt



y, sr = librosa.load(filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*"))), sr=16000)


