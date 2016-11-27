# ECG-GUI
Python GUI to import and analyze ECG signal
Please check the WIKI for more details.

This goal of this project is to import a biosignal(such as ECG, EMG or EEG) and analyze it. 
First, the GUI should allow the user to import raw data from csv or text file. 
Second, the program should allow filtering options on the signal. Most bioamplifiers 
result in noise (such as 60 hz from mains). The program should allow the implemention of 
several filters to remove 60 hz noise and high frequency noise (>110 hz depending on signal type)

Next, the program should plot both filtered and unfiltered signals. 

Additional features might include signal analysis such as HRV, inverse t-waves or other 
clinical abnormalities. One valuable feature would be bpm (beats per minute) algorithm
to calculate heart rate. 
