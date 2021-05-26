from tkinter import *
from F0_by_inz import *
from f0_spectrogram import *
from f0_autocorellation import *
from f0_zero_cross import *

# piękne ułatwienie za pomocą gui


# ------------------------------------------------------------------    OKNO WYBORU  
window = Tk()

# kolory przycisków
tpcolor = '#283655'
tpcolor_kliknij = '#212c45' #'#251e3e'
bgcolor2 = '#7A0008'
fgcolor = '#b3cde0'

top = Toplevel()
window.title("main")
window.geometry("400x500")
window.configure(bg=tpcolor)


# ------------------------------------------------------------------   FRAME

frame_title = Frame(master=window, width=40, height=120, bg = tpcolor)
frame_title.pack()

frame1 = Frame(master=window, width=700, height=120, bg = tpcolor)
frame1.pack()

frame_button = Frame(window,bg = tpcolor)
frame_button.pack(side=BOTTOM)

def fun1():
    print('TO DO............')

# ------------------------------------------------------------------   BUTTON


label_title = Label(frame_title,bg=tpcolor, fg=fgcolor, font = ("Times New Roman",14), pady = 10,  text = '\n[tytuł]', justify = CENTER)
label_title.pack()



# ------------------------------------------------------------------   amplituda

btn1 = Button(frame1, bg=tpcolor, fg=fgcolor, font = ("Times New Roman",10), pady = 10,  text=' Analiza przejśc przez 0 ',command=f0__zero_cross)
btn1.grid(row=1, column=0, padx=25, pady=20)

btn2 = Button(frame1, bg=tpcolor, fg=fgcolor, font = ("Times New Roman",10), pady = 10,  text=' Autokorelacja ',command=f0__autocorellation)
btn2.grid(row=1, column=1, padx=25, pady=20)

# ------------------------------------------------------------------   FFT inż 

btn3 = Button(frame1, bg=tpcolor, fg=fgcolor, font = ("Times New Roman",10), pady = 10,  text='  F0 inż  ',command=f0__pitch_contour_by_inz)
btn3.grid(row=2, column=0, padx=25, pady=20)

# ------------------------------------------------------------------   FFT spectro

btn4 = Button(frame1, bg=tpcolor, fg=fgcolor, font = ("Times New Roman",10), pady = 10,  text=' Spectrogram ',command= f0__spectrogram)
btn4.grid(row=3, column=0, padx=25, pady=20)



btn5 = Button(frame1, bg=tpcolor, fg=fgcolor, font = ("Times New Roman",10), pady = 10,  text=' Spectrogram welch ',command=f0__welch)
btn5.grid(row=3, column=1, padx=25, pady=20)

# ------------------------------------------------------------------   FFT różne

btn6 = Button(frame1, bg=tpcolor, fg=fgcolor, font = ("Times New Roman",10), pady = 10,  text=' yin ',command=fun1)
btn6.grid(row=4, column=0, padx=25, pady=20)

btn7 = Button(frame1, bg=tpcolor, fg=fgcolor, font = ("Times New Roman",10), pady = 10,  text=' power xxx ',command=fun1)
btn7.grid(row=4, column=1, padx=25, pady=20)

window.mainloop()