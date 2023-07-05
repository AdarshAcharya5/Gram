# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 19:44:06 2022

@author: Asus
"""

from tkinter import *
from PIL import ImageTk, Image

#Root Frame
root = Tk()

root.geometry("800x500")
root.configure(background="black")
root.title("Gram: grammar, made light")
root.resizable(False, False)
    
#Image Configurations
img = Image.open("G2.png")
resized = img.resize((350,350))
logo = ImageTk.PhotoImage(resized)
logolbl = Label(root, image=logo,background="black")
logolbl.place(x=227,y=-100)
    
#TextBoxes
tf = Text(root, height=3, width=50, background="black", foreground="white", insertbackground="white")
tf.place(x=195, y=210)
    
prompt = Label(root, text="Enter text here:", background="black", foreground="white", font=('@MS UI Gothic', 10))
prompt.place(x=193, y=190)
    
polarity = Label(root, text="Polarity: ", background="black", foreground="white", font=('@MS UI Gothic', 10))
polarity.place(x=195, y=270)
    
subjectivity = Label(root, text="Subjectivity: ", background="black", foreground="white", font=('@MS UI Gothic', 10))
subjectivity.place(x=195, y=290)
    
disclaimer = Label(root, text="An AI mini-project by Adarsh Acharya & Amogh Shet", background="black", foreground="white", font=('@MS UI Gothic', 8), fg='grey')
disclaimer.place(x=275, y=465)
    

root.mainloop()
