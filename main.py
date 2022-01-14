from tkinter import Tk, Canvas, mainloop

from jpg.functions import *
from jpg.jpg import JPG

TK_SILENCE_DEPRECATION = 1

if __name__ == "__main__":
    master = Tk()
    w = Canvas(master, width=800, height=800)
    w.pack()

    img = JPG("images/profile.jpeg")
    img.decode(w)

    mainloop()
