from tkinter import *
from F0_by_inz import *
from f0_spectrogram import *
from f0_autocorellation import *
from f0_zero_cross import *
from f0_welch_psd import *
from f0_yin import *

# Use this program to:
# 1. Upload a wave file of the sung audio
# 2. Select the method of frequency analysis in the graphical interface
# 3. Get a graph and information about the F0 value


# ------------------------------------------------------------------    WINDOW
window = Tk()

# kolory przycisków
tpcolor = '#283655'
tpcolor_kliknij = '#212c45'
bgcolor2 = '#7A0008'
fgcolor = '#b3cde0'

top = Toplevel()
window.title("main")
window.geometry("600x250")
window.configure(bg=tpcolor)

# ------------------------------------------------------------------   FRAME

frame_title = Frame(master=window, width=40, height=120, bg=tpcolor)
frame_title.pack()

frame1 = Frame(master=window, width=400, height=120, bg=tpcolor)
frame1.pack()

frame_button = Frame(window, bg=tpcolor)
frame_button.pack(side=BOTTOM)

# ------------------------------------------------------------------   BUTTON

label_title = Label(frame_title, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 14), pady=10,
                    text='\nChoose detection method of F0', justify=CENTER)
label_title.pack()

# ------------------------------------------------------------------   time

btn1 = Button(frame1, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 10), pady=10, text='Zero crossing analysis',
              command=f0__zero_cross)
btn1.grid(row=1, column=0, padx=25, pady=20)

btn2 = Button(frame1, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 10), pady=10, text=' Autocorellation ',
              command=f0__autocorellation)
btn2.grid(row=1, column=1, padx=25, pady=20)

# ------------------------------------------------------------------   FFT inż

btn3 = Button(frame1, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 10), pady=10,
              text='Method of engineering thesis', command=f0__pitch_contour_by_inz)
btn3.grid(row=2, column=0, padx=25, pady=20)

# ------------------------------------------------------------------   FFT spectro

btn4 = Button(frame1, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 10), pady=10, text=' Spectrogram ',
              command=f0__spectrogram)
btn4.grid(row=2, column=1, padx=25, pady=20)

# ------------------------------------------------------------------   FFT power

btn5 = Button(frame1, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 10), pady=10, text=' Spectrogram PSD ',
              command=f0__welch)
btn5.grid(row=2, column=2, padx=25, pady=20)

# ------------------------------------------------------------------   FFT różne

btn6 = Button(frame1, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 10), pady=10, text=' YIN ',
              command=fun__YIN)
btn6.grid(row=1, column=2, padx=25, pady=20)

window.mainloop()
