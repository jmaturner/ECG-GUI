import tkinter as tk
import numpy as np
import csv
from matplotlib import pyplot as plt
from matplotlib import style
from tkinter import *
import sounddevice as sd
import soundfile as sf



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

#gets the variable fs if entered
def getFs():
    global fs
    fs=samp.get()         
    print("The sampling frequency in Hz is %d" % fs )

#browse for path to data file
def uploaddata():
    global rawdata
    rawdata = filedialog.askopenfilename()
    print("data imported")
   

#for plotting single column data - creates time array from Fs
def plotdata():
    style.use('ggplot')
    v1=np.loadtxt(rawdata,unpack=True)
    samples=len(v1)
    t1=np.linspace(0,samples-1,samples)
    plt.plot(t1,v1)
    plt.title('Signal Plot')
    plt.ylabel('voltage')
    plt.xlabel('time')
    plt.show()

#plots two column data
def plotdata2():
    style.use('ggplot')
    t=np.loadtxt(rawdata,unpack=True,usecols=(0,))
    v=np.loadtxt(rawdata,unpack=True,usecols=(1,))  
    plt.plot(t,v)
    plt.title('Signal Plot')
    plt.ylabel('voltage')
    plt.xlabel('time')
    plt.show()

#plays the signal
def playit():
    try:
        global data
        data,fs=sf.read(rawdata)
        sd.play(data,fs)
    except:
        global snd
        snd=np.loadtxt(rawdata)
        sd.play(snd)
        
def stop():
    try:
        sd.stop(snd)
    except:
        sd.stop(data)
        
#Performs fft on data
def dofft(self):
    style.use('ggplot')
    try:
        data,fs=sf.read(rawdata)
        fft1=np.fft.fft(data)
        freqs=np.fft.fftfreq(len(fft1))
        inhertz=abs(freqs*fs)
        plt.plot(inhertz,abs(fft1))
        plt.title('Signal Spectrum FFT')
        plt.xlabel('Freq Hz')
        plt.ylabel('Power')
        plt.show()
    except:
        fs=samp.get()
        v = np.loadtxt(rawdata,unpack=True)
        fft1=np.fft.fft(v)
        freqs=np.fft.fftfreq(len(fft1))
        inhertz=abs(freqs*fs)
        plt.plot(inhertz,abs(fft1))
        plt.title('FFT')
        plt.xlabel('Freq Hz')
        plt.ylabel('Power')
        plt.show()
    



class StartPage(tk.Frame): #makes a new page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter fs if necessary", font=LARGE_FONT)
        label.grid(row=0,column=2,columnspan=4)

        #add button to enter Fs sampling freq
        global samp 
        samp=IntVar()
        mEntry = Entry(self, textvariable=samp).grid(row=1,column=3)     
        
        button1 = tk.Button(self, text="Submit Sample Freq",
                            command=getFs)
        button1.grid(row=1, column=2)
 
        #upload data button
        button2 = tk.Button(self, text="Upload a data file",
                            command=uploaddata)
        button2.grid(row=2, column=2)


        #single column data
        button3 = tk.Button(self, text="Plot Single Column data",
                            command=plotdata)
        button3.grid(row=4, column=2,pady=20)

        #two column data
        button5 = tk.Button(self, text="Plot two column data",
                            command=plotdata2)
        button5.grid(row=4, column=4)        
        #performs fft
        button6 = tk.Button(self, text="Plot the FFT",
                            command=lambda: dofft("this worked"))
        button6.grid(row=5, column=3)

        #button to play the signal
        button7 = tk.Button(self, text="Play it",
                            command=playit)
        button7.grid(row=7, column=3)
        button8 = tk.Button(self, text="stop",
                            command=stop)
        button8.grid(row=8,column=3)
        

        
        

app = sigapp()
app.mainloop()









