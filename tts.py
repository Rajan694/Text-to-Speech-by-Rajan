from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import pyttsx3
import os
import sys
from PIL import ImageTk, Image


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = Tk()
root.title("Text to Speech")
root.geometry("523x420")
root.resizable(False, False)
root.configure(bg='black')
raj=resource_path("tts.ico")
root.iconbitmap(raj)
eng = pyttsx3.init()
raj1=resource_path("listen.png")
raj2=resource_path("download.png")
raj3=resource_path("ttsimg.png")
photo1 = PhotoImage(file=raj1)
photo2 = PhotoImage(file=raj2)
img = Image.open(raj3)
img = img.resize((40, 40))
photo3 = ImageTk.PhotoImage(img)


def speak():
    text = tex.get(1.0, END)
    gender = gebox.get()
    speed = spbox.get()
    voices = eng.getProperty('voices')

    def setvoice():
        if gender == "Female":
            eng.setProperty("voice", voices[1].id)
            eng.say(text)
            eng.runAndWait()
        else:
            eng.setProperty("voice", voices[0].id)
            eng.say(text)
            eng.runAndWait()

    if text:
        if speed == "Fast":
            eng.setProperty("rate", 250)
            setvoice()
        elif speed == "Medium":
            eng.setProperty("rate", 150)
            setvoice()
        else:
            eng.setProperty("rate", 60)
            setvoice()


def download():
    text = tex.get(1.0, END)
    filen = ""
    if len(text) > 10:
        filen = text[:10]
    else:
        filen = text
    gender = gebox.get()
    speed = spbox.get()
    voices = eng.getProperty('voices')

    def setvoice():
        if gender == "Female":
            eng.setProperty("voice", voices[1].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            eng.save_to_file(text, filen + ".mp3")
            eng.runAndWait()
        else:
            eng.setProperty("voice", voices[0].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            eng.save_to_file(text, filen + ".mp3")
            eng.runAndWait()

    if text:
        if speed == "Fast":
            eng.setProperty("rate", 250)
            setvoice()
        elif speed == "Medium":
            eng.setProperty("rate", 150)
            setvoice()
        else:
            eng.setProperty("rate", 60)
            setvoice()


f1 = Frame(root, bg="grey", width=900, height=50)
f1.place(x=0, y=0)
Label(text="Text To Speech", font=("robota bold", 15), bg="grey", fg="blue").place(x=100, y=10)
Label(image=photo3).place(x=10, y=4)
tex = Text(root, font="arial 15", bg="white", wrap=WORD)
tex.place(x=10, y=60, width=500, height=250)
Label(text="Voice:", font=("robota bold", 15), bg="black", fg="Yellow").place(x=15, y=320)
Label(text="Speed:", font=("robota bold", 15), bg="black", fg="Yellow").place(x=250, y=320)
gebox = Combobox(root, values=["Female", "Male"], font=("arial", 13), state="r", width=10)
gebox.place(x=85, y=323)
gebox.set("Female")
spbox = Combobox(root, values=["Slow", "Medium", "Fast"], font=("arial", 13), state="r", width=10)
spbox.place(x=325, y=323)
spbox.set("Medium")
btn1 = Button(root, compound=LEFT, image=photo1, bg="black", width=35, command=speak)
btn1.place(x=15, y=370)
btn2 = Button(root, compound=LEFT, image=photo2, bg="black", width=35, command=download)
btn2.place(x=397, y=370)

root.mainloop()
