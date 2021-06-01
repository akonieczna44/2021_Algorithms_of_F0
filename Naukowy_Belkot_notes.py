import librosa, librosa.display
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np

# ------------------------------------------------------------------- INSTRUKCJA
# 1. nagraj wcześniej plik wave do wczytania
# 2. po otrzymaniu zapisu możesz je wygenerować na stronie http://lilybin.com/


# ------------------------------------------------------------------- SŁOWNIKI, BAZY

# wartości rytmiczne możliwe do przyporządkowania (nie ma trioli..... jeszcze xdd)
time_rythm = [0, 0.25, 0.375, 0.5, 0.75, 1, 1.5, 2, 3, 4]
rythm_sound = ["pauza", "16", "16.", "8", "8.", "4", "4.", "2", "2.", "1"]

rytm = {'wartosc': rythm_sound, 'czas': time_rythm}

hz_sound = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            65.4, 69.3, 73.4, 77.7, 82.4, 87.3, 92.5, 98, 103.8, 110, 116.5, 123.5,  # wielka
            130.8, 138.6, 146.8, 155.6, 164.8, 174.6, 185, 196, 207.7, 220, 233.1, 246.9,  # mała
            261.6, 277.2, 293.7, 311.1, 329.6, 349.2, 370, 392, 415.3, 440, 466.2, 493.8,  # razkreślna
            523.3, 554.36, 587.3, 622.25, 659.25, 698.5, 739.98, 783.9, 830.6, 880, 932.3, 987.7,  # dwukreślna
            1046.5, 1108.73, 1174.66, 1244.5, 1318.5, 1396.9, 1479.98, 1567.98, 1661.21, 1760, 1864.65,
            1975.53]  # trzykreślna

# to są nazwy dźwięków w gamie C-dur lub a-moll. miałam rozróżnianie tonacji, 
# ale Tobie będzie obojętne czy masz napisane "fis" czy "ges" ;)
name_Ca = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
"", "", "", "", "", "", "", "", "", "", "", "", "",
"c", "cis", "d", "es", "e", "f", "fis", "g", "gis", "a", "bes", "b", # 36-47 wielka #nie ma jej w wiolinowym
"c", "cis", "d", "es", "e", "f", "fis", "g", "gis", "a", "bes", "b",  # 48- 59 mała
"c'", "cis'", "d'", "es'", "e'", "f'", "fis'", "g'", "gis'", "a'", "bes'", "b'",  # 60-71 razkreślna
"c''", "cis''", "d''", "es''", "e''", "f''", "fis''", "g''", "gis''", "a''", "bes''", "b''", # 72-83 dwukreślna
"c'''", "cis'''", "d'''", "es'''", "e'''", "f'''", "fis'''", "g'''", "gis'''", "a'''", "bes'''", "b'''"# 84-95 trzykreślna
]

# ------------------------------------------------------------------- Marcin, tę wartość musisz sobie wpisać!!!
bpm = 95

# ------------------------------------------------------------------- funkcjami się nie przejmuj, jest ich sporo, ale cóż zrobić xddd
def Siatka_rytmiczna(slownik):
    # obliczam długości nut z czasów kliknięć
    # wrzucam wszystko do słownika docelowego z nutkami

    click = slownik['onset_times']
    dlugosci = []

    print('\n\nIlość nut ', len(click)-2)

    for index in range(len(click) - 1):
        el = click[index + 1] - click[index]
        dlugosci.append(el)

    # tylko dla tej metody obcinam 2 pierwsze
    dlugosci.pop(0)

    return dlugosci

def Dlugosci_wartosciRytm(dlugosci,bpm):
    # bpm essentia, która nie działa na Windowsie
    """
    dane_extractor, dane_extractor_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                                              rhythmStats=['mean', 'stdev'],
                                                              tonalStats=['mean', 'stdev'])(audio_file)
    print("BPM:", dane_extractor['rhythm.bpm'])
    bpm = dane_extractor['rhythm.bpm']
    """

    wartosc_rytm = []

    for index in range(len(dlugosci)):

        for i in range(len(rytm['czas'])):
            try:
                if rytm['czas'][i] * 60 / bpm < dlugosci[index] < rytm['czas'][i + 1] * 60 / bpm:  # bpm
                    odleglosc1 = dlugosci[index] - rytm['czas'][i]
                    odleglosc2 = rytm['czas'][i + 1] - dlugosci[index]

                    if odleglosc1 < odleglosc2:
                        wartosc_rytm.append(rytm['wartosc'][i])
                        break

                    elif odleglosc1 > odleglosc2:
                        wartosc_rytm.append(rytm['wartosc'][i + 1])
                        break
            except:
                print("błąd w obliczaniu wartości rytmicznych")

    return wartosc_rytm

def f_to_midi(srednie_wartosci_nut):
    numerki_midi = []
    for i in range(len(srednie_wartosci_nut)):

        for number in range(len(hz_sound)):
            fwiecej = round(1.029 * hz_sound[number], 2)
            fmniej = round(hz_sound[number] - (fwiecej - hz_sound[number]), 2)

            if fmniej < srednie_wartosci_nut[i] < fwiecej:
                numerki_midi.append(number)
    print('\nW midi to...', numerki_midi)

    # --------------------------------------------------------------------------------------- kontrola błędów oktawowych
    # jeśli jest oddalony od poprzedniego o ponad oktawę, to zniż go do dobrej oktawy
    def bledy_oktawowe(numerki_midi):

        start = 1  # zeby byla odleglosc okey

        for n in range(start, len(numerki_midi)):
            odleglosc = numerki_midi[n] - numerki_midi[n - 1]
            oktawy = int(odleglosc / 13)

            # błąd oktawowy, jeśli jest
            if oktawy != 0:
                numer = numerki_midi[n] - oktawy * 12

                numerki_midi[n] = numer
                start = n + 2  # omijam jedną odległość, żeby nie sprowadzić nuty obok do złej oktawy

        return numerki_midi

    numerki_midi = bledy_oktawowe(numerki_midi)
    return numerki_midi

def nazwy_nutek(numerki_midi, name_sound):
    nazwy = []
    for i in range(len(numerki_midi)):
        current = name_sound[numerki_midi[i]]
        nazwy.append(current)
    print('\n\nDźwięki...', nazwy)
    return nazwy

def midiRythm_toLily(name, rythm, adr):

    nuty = []
    try:
        for i in range(len(name)):
            if rythm[i] != "pauza":  # jeśli jest różne od pauzy
                nuty.append(name[i] + rythm[i])
    except:
        print('błąd w midirythm to lily')

    print('\n\nNuty do kopiowania na stronę lilybin [pionowo]')

    for n in range(len(nuty)):
        print(nuty[n])


    # dodawanie metrum
    # metrumm = input(str("wpisz metrum (liczba/ jakich wartości): "))
    # automatyczne
    metrumm = '4/4'

    w2 = "\\time"
    ttime = w2[0] + w2[1] + w2[2] + w2[3] + w2[4] + metrumm + " "

    # dodawanie tonacji - na razie ręcznie, bo essentia nie jest wspierana na Windowsie
    """
    dane_extractor, dane_extractor_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                                              rhythmStats=['mean', 'stdev'],
                                                              tonalStats=['mean', 'stdev'])(adr)
    t = dane_extractor['tonal.key_edma.key']
    k = dane_extractor['tonal.key_edma.scale']
    """

    t = 'C'
    k = 'major'

    poczatek = "{" + ttime # + ton_key
    for n in nuty:
        poczatek = poczatek + n + " "

    nuty_opis = poczatek + "}"

    # podmieniam nuty, żeby one były jednak samym stringiem, a nie listą
    nuty_same = " "
    for i in nuty:
        nuty_same = nuty_same + str(i) + " "

    print('\nNuty do kopiowania z metrum: ', nuty_opis)
    print('\nNuty same', nuty_same)
    return nuty_opis, nuty_same

# ------------------------------------------------------------------- GWÓŹDŹ PROGRAMU
def seg_librosa():

    # ------------------------------------------------------------------- wybór pliku
    audio_file = filedialog.askopenfilename(title="Wybierz plik", filetypes = (("wav mono files",".wav"), ("all files", "*.*")))
    y, sr = librosa.load(audio_file)

    # ------------------------------------------------------------------- główny słownik na nuty, bo nie jest to jeszcze obiektowe xd
    nutyLib = {}

    # początki nut - wykrywanie miejsc peaks
    hop_length = 256 #256 # 100 - 300
    nutyLib['onset_env'] = librosa.onset.onset_strength(y, sr=sr, hop_length=hop_length)

    nutyLib['onset_samples'] = librosa.onset.onset_detect(y, sr=sr, units='samples',
                                               hop_length=hop_length, backtrack=False,
                                               pre_max=20, post_max=20,
                                               pre_avg=100,post_avg=100,
                                               delta=0.05,wait=0) #0.1 było normalnie XD

    # sample, ale z granicami
    nutyLib['onset_boundaries'] = np.concatenate([[0], nutyLib['onset_samples'], [len(y)]])

    # "kliknięcia"
    nutyLib['onset_times'] = librosa.samples_to_time(nutyLib['onset_boundaries'], sr=sr)
    x_onset = np.linspace(0, len(y)/sr, len(nutyLib['onset_env']))

    plt.subplot(211)
    plt.plot(x_onset, nutyLib['onset_env'])
    plt.ylabel('Siła zmian energii',fontsize=10)
    plt.xlabel('Czas [s]',fontsize=10)
    plt.title('Wykryte początki nut')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlim(0,20)
    #plt.xlim(0, len(nutyLib['onset_env'])/sr)

    plt.subplot(212)
    librosa.display.waveplot(y)
    plt.vlines(nutyLib['onset_times'], -1, 1, color='r')
    plt.ylabel('Amplituda',fontsize=10)
    plt.xlabel('Czas [s]',fontsize=10)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlim(0,20)
    plt.show()


    # pitch
    def estimate_pitch(segment, sr, fmin=50.0, fmax=2000.0):

        r = librosa.autocorrelate(segment)

        # zakres auto
        i_min = sr / fmax
        i_max = sr / fmin

        # append, del
        r[:int(i_min)] = 0
        r[int(i_max):] = 0

        # max
        i = r.argmax()
        f0 = float(sr) / i
        return f0

    def estimate_pitch_and_generate_sine(y, onset_samples, sr):
        for i in range(len(nutyLib['onset_boundaries']) - 1):
            n0 = onset_samples[i]
            n1 = onset_samples[i+1]
            f0 = estimate_pitch(y[n0:n1], sr)
            nuty_hz.append(f0)

        return nuty_hz

    nuty_hz = []
    nutyLib['nameLily'] = estimate_pitch_and_generate_sine(y, nutyLib['onset_boundaries'], sr=sr)

    # pierwszy element
    nutyLib['nameLily'].pop(0)

    nutyLib['midi'] = f_to_midi(nutyLib['nameLily'])
    nutyLib['nameLily'] = nazwy_nutek(nutyLib['midi'], name_Ca)

    nutyLib['dlugosci'] = Siatka_rytmiczna(nutyLib)

    nutyLib['rythmLily'] = Dlugosci_wartosciRytm(nutyLib['dlugosci'],bpm) # szesnatska, 0.25

    nutyLib['generate_opis'],nutyLib['generate'] = midiRythm_toLily(nutyLib['nameLily'],nutyLib['rythmLily'],audio_file)


    # to jest do późniejszego generowania zapisu
    # print('\nSkopiuj i generuj', nutyLib['generate_opis'], '\n')

    return nutyLib


seg_librosa()


# slownik = seg_librosa()

# okno3_wyniki(slownik)