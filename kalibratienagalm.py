# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 13:59:53 2025

@author: joran
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
file_path = "Data/Metingen/vak11-meting3.wav"
sampling_rate, audio_data = wavfile.read(file_path)
nulmeting = 10
tijdsinterval = 0.5

# Inlezen van het .wav bestand
 
center_freq = 600
bandwidth = 200

# Ontwerp een bandpass filter
def butter_bandpass(center_freq, bandwidth, fs, order=4):
    nyquist = 0.5 * fs
    low = (center_freq - bandwidth / 2) / nyquist
    high = (center_freq + bandwidth / 2) / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Pas het bandpassfilter toe op de audio data
b, a = butter_bandpass(center_freq, bandwidth, sampling_rate)
filtered_audio_data = filtfilt(b, a, audio_data)

# Tijd-array maken
duration = len(audio_data) / sampling_rate
time = np.linspace(0., duration, len(audio_data))

# Bepaal de grootte van het tijdsinterval bij het voortschrijdend gemiddelde
window_size = int(tijdsinterval * sampling_rate) 

# Bereken het voortschrijdend gemiddelde van de absolute waarde van de amplitude
rolling_avg = np.convolve(np.abs(filtered_audio_data), np.ones(window_size)/window_size, mode='same')
#correctie op het aantal dB
db = 20 * np.log10(rolling_avg)/0.78
#de max, index van de max en de starttijd
dbpeak = max(db)
dbpeakindex = np.argmax(db)
tbegin = time[dbpeakindex]
waardelijst = [60,30,20,10]
#bepalen wat de best mogelijke optie is om de nagalmtijd te bepalen (-60,-30,-20,-10)
for i,x in enumerate(waardelijst):
    if(dbpeak-x>nulmeting+1):
        breakvalue= dbpeak-x
        a = i
        break
    
#nagalmtijd berekenen aan de hand van welk waarde bepaald is
for i,x in enumerate(db):
    if(i>dbpeakindex and x<breakvalue):
        if(a==0):
            nagalmtijd = time[i]-tbegin
            print(time[i],tbegin)
            break
        elif(a==1):
            nagalmtijd= (time[i]-tbegin)*2
            print(time[i],tbegin)
            break
        elif(a==2):
             nagalmtijd= (time[i]-tbegin)*3
             print(time[i],tbegin)
             break
        elif(a==3):
            nagalmtijd= (time[i]-tbegin)*6
            print(time[i],tbegin)
            break
#plotten van de grafiek
plt.plot(time,db)
plt.show()
        