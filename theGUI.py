# -*- coding: utf-8 -*-
"""
Author - John Turner
version1.1
"""

import tkinter as tk
from tkinter import *
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style
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
    global fs, nyq
    fs=samp.get()   
    nyq=0.5*fs      
    print("The sampling frequency in Hz is %d" % fs )
    print("The Nyquist Frequency is %d" % nyq)

def getFcl():
    global fcl
    fcl = fc1.get()
    print(fc1.get())

def getFch():
    global fch
    fch = fc2.get()
    print(fc2.get())    

#this function allows the user to browse for the data file
def uploaddata():
    global rawdata
    rawdata = tk.filedialog.askopenfilename()
    print("data imported")

    
#highpass filter - parameters will be passed from user at GUI    
#scaled to accomodate any Fs
#e.g 0.05 represents 15 hz for 600 Hz signal
def plotfiltdata():
    v1=np.loadtxt(rawdata,unpack=True)
    samples=len(v1)
    t1=np.linspace(0,samples-1,samples)
    fc = fc1.get()
    low=fc/nyq  #fc = cutoff
    b,a=signal.butter(6,low,'high')
    y=signal.filtfilt(b,a,v1)
    plt.plot(t1,y,'r',t1,v1,'k')
    plt.title('Signal Plot')
    plt.ylabel('voltage')
    plt.xlabel('time')
    plt.show()

     
#plots data that has time and voltage
def plotdata():
    style.use('ggplot')
    if CheckVar1.get() == 0:
        print(CheckVar1.get())
        v1=np.loadtxt(rawdata,unpack=True)
        samples=len(v1)
        t1=np.linspace(0,samples-1,samples)
        plt.plot(t1,v1)
    else:
        print(CheckVar1.get())
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
        
#performs fft on data
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
        plt.title('Signal Spectrum FFT')
        plt.xlabel('Freq Hz')
        plt.ylabel('Power')
        plt.show()
    


#makes a new page
class StartPage(tk.Frame): 

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Signal Processing Tool V1.0", font=LARGE_FONT)
        label.grid(row=0,column=2,columnspan=4)

        #add button to enter Fs sampling freq
        global samp 
        samp=tk.IntVar()
        mEntry = Entry(self, textvariable=samp).grid(row=1,column=3)     
        
        button1 = tk.Button(self, text="Submit Sample Freq",command=getFs)
        button1.grid(row=1, column=2)
        
        global fc1, fc2
        fc1 = tk.IntVar()
        fc2 = tk.IntVar()
        Fc1Entry = Entry(self, textvariable=fc1).grid(row=3,column=5)     
        Fc2Entry = Entry(self,textvariable=fc2).grid(row=4,column=5)
        buttonfc1 = tk.Button(self, text="Submit Fc1",command=getFcl)
        buttonfc2 = tk.Button(self, text="Submit Fc2",command=getFch)
        buttonfc1.grid(row=3, column=4)
        buttonfc2.grid(row=4, column=4)
        
        #checkbox for two-column data
        global CheckVar1
        CheckVar1 = IntVar()
        C1 = tk.Checkbutton(self,text="data contains time", variable=CheckVar1,onvalue=1,offvalue=0)
        C1.grid(row=2,column=3)      
        
        #upload data button
        button2 = tk.Button(self, text="Upload a data file",command=uploaddata)
        button2.grid(row=2, column=2, pady=20)

        #single column data
        button3 = tk.Button(self, text="Plot time domain",command=plotdata)
        button3.grid(row=3, column=2,pady=20)    
        
        #performs fft
        button6 = tk.Button(self, text="Plot FFT", command=lambda: dofft("this worked"))
        button6.grid(row=3, column=3)

        #stop and play buttons
        button7 = tk.Button(self, text="Play", command=playit)
        button7.grid(row=7, column=3, pady=15)
        button8 = tk.Button(self, text="stop", command=stop)
        button8.grid(row=7,column=2, pady=15)
           
        #Plot filtered data
        button10 = tk.Button(self, text="Plot Filtered Signal", command=plotfiltdata)
        button10.grid(row=4, column=3)             
        

app = sigapp()
app.mainloop()




