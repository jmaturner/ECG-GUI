import tkinter as tk
import numpy as np
import csv
from matplotlib import pyplot as plt
from matplotlib import style
from tkinter import *


LARGE_FONT = ("Verdana", 12)

class sigapp(tk.Tk):

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

#this function allows the user to browse for the data file
def uploaddata():
    global rawdata
    rawdata = filedialog.askopenfilename()
    print("data imported")
    

#for plotting single column data - creates time array from Fs
def plotdata():
    style.use('ggplot')
    v1=np.loadtxt(rawdata,unpack=True)
    #elapsedtime=samples*1/Fs
    samples=len(v1)
    t1=np.linspace(0,samples-1,samples)
    plt.plot(t1,v1)
    plt.title('Signal Plot')
    plt.ylabel('voltage')
    plt.xlabel('time')
    plt.show()

#plots data that has time and voltage
def plotdata2():
    style.use('ggplot')
    t=np.loadtxt(rawdata,unpack=True,usecols=(0,))
    v=np.loadtxt(rawdata,unpack=True,usecols=(1,))  
    plt.plot(t,v)
    plt.title('Signal Plot')
    plt.ylabel('voltage')
    plt.xlabel('time')
    plt.show()

#this function performs fft on data
def dofft(self):
    style.use('ggplot')
    t,v = np.loadtxt(rawdata,unpack=True)
    fft1=np.fft.fft(v)
    freqs=np.fft.fftfreq(len(fft1))
    inhertz=abs(freqs*Fs)
    
    v1 = np.loadtxt(rawdata,unpack=True)
    fft1=np.fft.fft(v)
    freqs=np.fft.fftfreq(len(fft1))
    inhertz=abs(freqs*Fs)    

    plt.plot(inhertz,abs(fft1))
    plt.title('Signal Spectrum FFT')
    plt.xlabel('Freq Hz')
    plt.ylabel('Power')
    plt.show()


def getFs():
    global Fs
    Fs=samp.get()         
    print("The sampling frequency in Hz is %d" % Fs )



class StartPage(tk.Frame): #makes a new page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Entery Sampling Frequency First", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        #add button to enter Fs sampling freq
        global samp 
        samp=IntVar()
        mEntry = Entry(self, textvariable=samp).pack()     
        
        button1 = tk.Button(self, text="Submit Sample Freq",
                            command=getFs)
        button1.pack(pady=10,padx=10)
 
        #add button to plot single column data - voltage only
        button2 = tk.Button(self, text="Upload a data file",
                            command=uploaddata)
        button2.pack(pady=10,padx=10)

        #add button that handles 2 column, time, voltage data
        button3 = tk.Button(self, text="Plot Single Column data",
                            command=plotdata)
        button3.pack(pady=10,padx=10)

        #add button to execute function plotdata
        button4 = tk.Button(self, text="Plot two column data",
                            command=plotdata2)
        button4.pack(pady=10,padx=10)        

        #add button to perform FFT on data
        button5 = tk.Button(self, text="Perform the FFT and plot",
                            command=lambda: dofft("this worked"))
        button5.pack(pady=10,padx=10)
        

        
        

app = sigapp()
app.mainloop()









