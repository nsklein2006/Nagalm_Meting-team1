# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 10:54:36 2025

@author: joran
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
#aantal metingen invoeren en variabelen
nmeting = 5
nwaardes = 2
iwaardes = 1
imeting =1
#waardes van het gekalibreerde apparaat
waardelijst = [94.11,114.15]
#maken van lege lijsten
dBmetinglijst = []
stdevlijst = []
dBlijstgemiddeld = []
#uitrekenen van de rauwe dB waardes
for x in range(nmeting*nwaardes):
    if imeting>nmeting:
        imeting=1
        iwaardes+=1
        stdevlijst.append(np.std(dBmetinglijst))
        dBlijstgemiddeld.append(np.mean(dBmetinglijst))
        print(dBmetinglijst)
        dBmetinglijst = []
        
        
        
    file_path = f'Data/Kalibratie/waarde{iwaardes}-meting{imeting}.wav'  
    sampling_rate, audio_data = wavfile.read(file_path)

    # Stel de lengte van het tijdsinterval in
    tijdsinterval = 0.5

    # Stel de middenfrequentie en bandbreedte van de bandfilter in
    center_freq = 1000
    bandwidth = 20  

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
    db = 20 * np.log10(rolling_avg)

    # Time range from 2 to 4 seconds
    start_time = 0
    end_time = 10

    # Extract the time and corresponding db values for the specified range
    time_range = (time >= start_time) & (time <= end_time)
    filtered_time = time[time_range]
    filtered_db = db[time_range]
    dBmetinglijst.append(np.mean(filtered_db))
    #print(dBmetinglijst)
    imeting+=1
#toevoegen van de waardes een laatste keer
stdevlijst.append(np.std(dBmetinglijst))
dBlijstgemiddeld.append(np.mean(dBmetinglijst))
#printen van de waardes
print(dBlijstgemiddeld)
print(stdevlijst)
x_fit = np.linspace(0, 120, 100)  # Create a range from 0 to 120
y_fit = x_fit  # y = x, which is a line with slope 1

plt.plot(x_fit, y_fit, linestyle = "--", label='Direct Fit: y = x', color='green')
X = np.array(waardelijst)
y = np.array(dBlijstgemiddeld)

# Calculate the slope (m) with the formula m = sum(x_i * y_i) / sum(x_i^2)
slope = np.dot(X, y) / np.dot(X, X)  # This is the least squares solution for slope

# Create the fitted line (y = mx)
fit_line_waardelijst = slope * X

# Plot the data with error bars
plt.errorbar(waardelijst, dBlijstgemiddeld, yerr=stdevlijst, fmt='o', color='blue', ecolor='red', capsize=5, label='Data with Error Bars')

# Plot the direct fit through the origin
plt.plot(X, fit_line_waardelijst, linestyle ="--", label=f'Fit: y = {slope:.2f} * x', color='red')

# Customize the plot
plt.xlabel("Werkelijke dB")
plt.ylabel("Gemeten dB")
plt.grid()
plt.title("Kalibratie Grafiek")
plt.legend()

plt.show()
