# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 17:48:02 2017

@author: Hossam
Modified by Enxiao Reza 2021-4-22
"""

#%% Plotting the IV curve of the heaters using Keithley

#baseFolder = 'S:/Dropbox (SiEPIC)/SiEPIC_Team/Jing/Measurements/'
baseFolder = 'S:/Users/Edison/Huawei-Grouse-measurement/python-result'
# load all required libraries
import numpy as np # NumPy is the fundamental package for scientific computing with Python
import time
import matplotlib.pyplot as plt
#from time import *

from scipy.io import savemat
from scipy.io import loadmat

from datetime import datetime

if 1:
    import hp816x_N77Det_instr
    reload(hp816x_N77Det_instr)
    laser = hp816x_N77Det_instr.hp816x_N77Det();
    laser.connect('GPIB0::20::INSTR','TCPIP0::100.65.11.185::inst0::INSTR', reset=0, forceTrans=1)
    #Address = TCPIP0::100.65.11.185::inst0::INSTR
    
if 0:
    import hp816x_instr
    reload(hp816x_instr)
    laser = hp816x_instr.hp816x();
    laser.connect('GPIB0::20::INSTR', reset=0, forceTrans=1)


#Setting up part 1 of sweep parameters
central_wavelength = 1500e-9
sweep_range = 14e-9
time.sleep(6.0)  # gives the laser some time to connected

c = 299792458
laser.setTLSState('on');  # turn on laser

laser.setAutorangeAll()
laser.setTLSWavelength(central_wavelength)

laser.setPWMPowerUnit(1, 0, 'dBm')

laser.setAutorangeAll()
laser.setTLSWavelength(central_wavelength)

# Initialize sweep laser
laser.sweepNumScans = 1;
laser.sweepStepWvl = 8e-12;
laser.sweepStartWvl = central_wavelength - sweep_range;  # Starting wavelength
laser.sweepStopWvl = central_wavelength + sweep_range;  # Stopping wavelength
laser.sweepSpeed = '5nm';
#laser.sweepLaserOutput = 'lowsse';
laser.sweepLaserOutput = 'highpower';
laser.sweepUnit = 'dBm';
laser.sweepPower = -10;
laser.sweepInitialRange = -10
sweepUseClipping = 1;
sweepClipLimit = -70;
power_thru = []
power_drop = []

start_time = time.time()

### HERE ### - power array has to return 6 indeces
(wavelength,power) = laser.sweep(); 

print("Sweep time = ",(time.time() - start_time) ,"seconds")  ## Take note- this is how to time things in python

# Change power units to dBm after sweep
laser.setAutorangeAll()

#Getting the power channels from the sweep output
power_chan1 = power[:, 0]
power_chan2 = power[:, 1]
power_chan3 = power[:, 2]  #Seems like we could have multiple channels, this could be useful for future layouts.
power_chan4 = power[:, 3]
power_chan5 = power[:, 4]
power_chan6 = power[:, 5]

#Showing a plot of the initial sweep:
plt.figure()
plt.plot(wavelength*1e9,power_chan1,'b', label = 'Power1')
plt.plot(wavelength*1e9,power_chan2,'r', label = 'Power2')
plt.plot(wavelength*1e9,power_chan3,'g', label = 'Power3')
plt.plot(wavelength*1e9,power_chan4,'k', label = 'Power4')
plt.plot(wavelength*1e9,power_chan5,'c', label = 'Power5')
plt.plot(wavelength*1e9,power_chan6,'m', label = 'Power6')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Power (dBm)')
plt.legend()
plt.show()

# Change power units to dBm after sweep

laser.setAutorangeAll()
laser.setTLSWavelength = central_wavelength;

# %%  Debug
laser.disconnect();