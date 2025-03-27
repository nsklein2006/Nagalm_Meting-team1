# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 19:51:21 2025

@author: joran
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
import seaborn as sn 
#declareren variabelen en lijsten
nmeting = 3
nwaardes = 36
iwaardes = 1
imeting =1
rijwaarde = 1
nulmeting =10
nagalmmetinglijst = []
nagalmavgvak = []
nagalmrij = []
stdlijst =[]
#loopen over elk bestand
for x in range(nmeting*nwaardes):
    if(imeting>nmeting):
        iwaardes+=1
        imeting =1
        nagalmrij.append(np.mean(nagalmavgvak))
        stdlijst.append(np.std(nagalmavgvak))
        nagalmavgvak = []
        rijwaarde+=1
        if(rijwaarde>6):
            rijwaarde=1
            nagalmmetinglijst.append(nagalmrij)
            nagalmrij=[]

        
        
        
        
    file_path = f'Data/Metingen/vak{iwaardes}-meting{imeting}.wav' 
    sampling_rate, audio_data = wavfile.read(file_path)
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
    #Omrekenen naar dB met coorectie    
    db = 20 * np.log10(rolling_avg)/0.78
    #bepalen van de piek, index van de piek en de starttijd
    dbpeak = max(db)
    dbpeakindex = np.argmax(db)
    tbegin = time[dbpeakindex]
    #mogelijke waardes om de nagalmtijd te berekenen
    waardelijst = [60,30,20,10]
    #bepaal welke waarde je gebruikt voor de nagalmtijd
    for i,x in enumerate(waardelijst):
        if(dbpeak-x>nulmeting+1):
            breakvalue= dbpeak-x
            a = i
            break
        
    #berekenen van de nagalmtijd aan de hand van de gekozen waarde
    for i,x in enumerate(db):
        if(i>dbpeakindex and x<breakvalue):
            if(a==0):
                nagalmtijd = time[i]-tbegin
                print(nagalmtijd)
               # print(time[i],tbegin)
                break
            elif(a==1):
                nagalmtijd= (time[i]-tbegin)*2
                print(nagalmtijd)
               # print(time[i],tbegin)
                break
            elif(a==2):
                 nagalmtijd= (time[i]-tbegin)*3
                 print(nagalmtijd)
                 #print(time[i],tbegin)
                 break
            elif(a==3):
                nagalmtijd= (time[i]-tbegin)*6
                print(nagalmtijd)
                #print(time[i],tbegin)
                break
    nagalmavgvak.append(nagalmtijd)
    imeting+=1
#toevoegen van de lijsten 1 laatste keer 
nagalmrij.append(np.mean(nagalmavgvak))
nagalmmetinglijst.append(nagalmrij)
#printen van waardes
print(nagalmmetinglijst)
print("\n")
print(stdlijst)
#heatmap maken
sn.heatmap(nagalmmetinglijst,annot=True,cmap="Reds",cbar_kws={'label': 'nagalmtijd (s)'})
plt.show()