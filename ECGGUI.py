import tkinter as tk
import numpy as np
import csv
from matplotlib import pyplot as plt
from matplotlib import style
from tkinter import *


LARGE_FONT = ("Verdana", 12)

class ecgapp(tk.Tk):

    def __init__(self,*args,**kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container,self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="snew")



        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

#this function should allow the user to browse for a txt raw data ECG file
#This also should declare the t,v variable 
def uploaddata(self):
    global ecgdata
    ecgdata = filedialog.askopenfilename()
    #t,v = ecgdata(unpack=True)
    #t,v=ecgdata
    print("data imported")
    
#def Fs(self)
    #user enters sampling frequency


#functions for buttons
def plotecg(self):
    style.use('ggplot')
    t,v = np.loadtxt(ecgdata,unpack=True)
    global samples
    samples=len(v)
    global Fs
    Fs=200
    time = (samples/Fs)
    plt.plot(t,v)
    plt.title('ECG')
    plt.ylabel('voltage')
    plt.xlabel('time')
    plt.show()

#this function performs fft on data
def dofft(self):
    style.use('ggplot')
    t,v = np.loadtxt(ecgdata,unpack=True)
    fft1=np.fft.fft(v)
    Fs=400
    freqs=np.fft.fftfreq(len(fft1))
    inhertz=abs(freqs*Fs)
    plt.plot(inhertz,abs(fft1))
    plt.title('Signal Spectrum FFT')
    plt.xlabel('Freq Hz')
    plt.ylabel('Power')
    plt.show()

def getFs(self):
    data=IntVar()
    Fs=data.get()

class StartPage(tk.Frame): #makes a new page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Browse for data file", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        #allows user to enter sampling rate
        data=IntVar()
        entry = Entry(textvariable=data)
        entry.pack(pady=10,padx=10)
        entry.bind("<Return>", getFs)
        
        #add button to execute function plotecg
        button1 = tk.Button(self, text="Upload a data file",
                            command=lambda: uploaddata("this worked"))
        button1.pack(pady=10,padx=10)
        #add button to execute function plotecg
        button2 = tk.Button(self, text="Plot the data in time domain",
                            command=lambda: plotecg("this worked"))
        button2.pack(pady=10,padx=10)
        
        #add button to perform FFT on data
        button3 = tk.Button(self, text="Perform the FFT and plot",
                            command=lambda: dofft("this worked"))
        button3.pack(pady=10,padx=10)

        #add button to perform filter on data
        button4 = tk.Button(self, text="Perform Filter",
                            command=lambda: welch("this worked"))
        button4.pack(pady=10,padx=10)


app = ecgapp()
app.mainloop()









