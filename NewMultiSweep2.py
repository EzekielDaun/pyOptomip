## This was originally written by Michael Caverley in 2015
## Code has been modified by Eric Lyall in December 2020 ericlyall1428@gmail.com
## It was modified for the 8164A laser set-up at the Life Sciences Institute at UBC. The laser has 2 active detectors.
## An option for a periodic fine align is/has been added
## 2021-03-31 S. Grist added saving the timestamp associated with each sweep to a CSV.

## Import Statements:

import hp816x_instr
reload(hp816x_instr)

import matplotlib.pyplot as plt
from scipy.io import savemat
import time
from fineAlign import fineAlign
from CorvusEco import CorvusEcoClass
import os
import visa
import numpy as np
import time
import csv

def calc_slice_indices (wavelength, guess_wavelength,range):
    st_index = int((guess_wavelength-range - wavelength[0])/(wavelength[len(wavelength)-1]-wavelength[0])*len(wavelength))
    end_index = int((guess_wavelength+range - wavelength[0])/(wavelength[len(wavelength)-1]-wavelength[0])*len(wavelength))
    return st_index,end_index

def find_optimum_wavelength(matdict, guess_wavelength=1500e-9,range=2e-9):
    #Trying to find a good wavelength to fine align to.
    #Do this by searching for the highest combined power readings withing +- range of a guessing wavelength
    #For example, if the guess wavelength was 1550 and rage 2, would look for the highest combined power reading from
    #1548 to 1552 nm, and then return this wavelength to do a fine alignment.

    wavelength = np.array(matdict['wavelength']) # retrieving the wavelengths used during the sweep (nm)
    power1 = np.array(matdict['power1'])        # retrieving the values for the power1 channel. (dBm)
    power2 = np.array(matdict['power2']) # retrieving the values for the power2 channel. (dBm)
    #Finding the range (by array index) to look for max combined power
    st_index, end_index = calc_slice_indices(wavelength,guess_wavelength,range)
    #Creating an array with added power, tha only looks at the previously specified range.
    combo_power = np.add(power1,power2)[st_index:end_index]

    max_index = combo_power.argmax() + st_index # returns the first incidence of the maximum value.

    optimum_wavelength = wavelength[max_index]

    print(optimum_wavelength)

    return optimum_wavelength

def run_fine_align(laser, stage, optimum_wavelength=1500e-9):
    """
    Runs a fine align, moving the stage around to optimize power readings
    :param laser: A connected laser
    :param stage: A connected stage
    :param optimum_wavelength: The wavelength you would like to do the fine align around. This doesn't actually do
    anything yet, as teh fineAlign wavelength gets re-defined in the fineAlign code.
    :return:
    """
    laser.setAutorangeAll()
    laser.setTLSWavelength(optimum_wavelength)    #Setting the laser to optimum wavelength before alignment
    print("Did the wavelegnth change to: ", optimum_wavelength*1e9)

    Align= fineAlign(laser, stage)  #Creating a new finAlign object
    Align.wavelength = optimum_wavelength

    #Want to print out the power before fine alignment:
    detectorPriority = [0, 1]
    for det in detectorPriority:
        detSlot = Align.laser.pwmSlotMap[det][0]
        detChan = Align.laser.pwmSlotMap[det][1]
        power = Align.laser.readPWM(detSlot, detChan)
        print("Detector", det, "Before fine align Power = ", power,"\n")

    #Doing the actual fine Align - this is currently automatically set to 1550
    print("Starting fine align...")
    # Align.laser.ctrlPanel.laserPanel.laserPanel.haltDetTimer()
    Align.doFineAlign()

    # Getting power after fine alignment
    for det in detectorPriority:
        detSlot = Align.laser.pwmSlotMap[det][0]
        detChan = Align.laser.pwmSlotMap[det][1]
        power = Align.laser.readPWM(detSlot, detChan)
        print("Detector", det, "After fine align Power = ", power,"\n")

    return


## Main script running here:

if __name__ == '__main__':

    #Setting up part 1 of sweep parameters
    central_wavelength = 1507e-9
    sweep_range = 7e-9

    ## Connecting to the laser

    laser = hp816x_instr.hp816x();
    laser.connect('GPIB0::20::INSTR', reset=0, forceTrans=1) ## This is the address of the GPIB cable we are using,from NI MAX
    time.sleep(6.0)  # gives the laser some time to connece

    c = 299792458
    laser.setTLSState('on');  # turn on laser

    laser.setAutorangeAll()
    laser.setTLSWavelength(central_wavelength)


    laser.setPWMPowerUnit(1, 0, 'dBm')

    #Connecting to the stage for fun:
    Stage = CorvusEcoClass()
    Stage.connect(visaName='ASRL4::INSTR',rm=visa.ResourceManager(),Velocity= 5, Acceleration=500, NumberOfAxis=3)

    laser.setAutorangeAll()
    laser.setTLSWavelength(central_wavelength)

    #Settting the base folder- this is where sweeps will save into

    # baseFolder = 'C:/Users/eric1/Google Drive/UBC/CBR/Vinny COVID Project/Dec9Trial2/'
    baseFolder = 'C:/Users/MapleLeafStage/Documents/2021-11-03_Detergent_Testing_7X/'


    ## Setting up swee parameters:

    laser.sweepStartWvl = central_wavelength-sweep_range;  #Starting wavelength

    laser.sweepStopWvl = central_wavelength+sweep_range; #Stopping wavelength

    laser.sweepStepWvl = 1e-11;  # step size

    laser.sweepNumScans = 1; ## I **think** the laser can average out over 1, 2 or 3 scans.

    laser.sweepSpeed = '5nm';   # '5nm' is the only sweep speed that currently works. The laser is capable of '40nm' and '.5nm',
                                # but this software is not

    laser.sweepLaserOutput = 'highpower';

    laser.sweepPower = 0;  #Always set this to 0

    laser.sweepInitialRange = -20


    #Running an initial sweep on the laser:
    start_time = time.time()
    (wavelength, power) = laser.sweep();
    print("Sweep time = ",(time.time() - start_time) ,"seconds")  ## Take note- this is how to time things in python

    # Change power units to dBm after sweep
    laser.setAutorangeAll()
    # laser.setTLSWavelength = 1550e-9;

    #Getting the power channels from the sweep output

    power_chan1 = power[:, 0]
    power_chan2 = power[:, 1]
    #power_chan3 = power[:, 2]  #Seems like we could have multiple channels, this could be useful for future layouts.
    #power_chan4 = power[:, 3]

    #Showing a plot of the initial sweep:

    plt.figure()
    plt.plot(wavelength*1e9,power_chan1, 'b', label = 'Power1')
    plt.plot(wavelength*1e9,power_chan2,'r', label = 'Power2')
    #plt.plot(wavelength*1e9,power_chan3,'g', label = 'Power3')
    #plt.plot(wavelength*1e9,power_chan4,'k', label = 'Power4')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Power (dBm)')
    plt.legend()
    plt.show()

    ## Getting into running multiple sweeps:

    #Choosing the number of scans to preform. This affects how long the program runs for.

    nbscan=5000;

    # get the initial time
    t0 = time.time()

    for i in range(1,nbscan+1):
        # get elapsed time
        t1 = time.time()
        t_elapse = t1-t0

        matFilename = 'laser_sweep_%d.mat' %i;

        # save elapsed time to CSV
        csvFilename = 'timeSteps.csv'
        with open(baseFolder+csvFilename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([i, matFilename, t_elapse])

        # sweep laser

        (wavelength, power) = laser.sweep();

        power_chan1 = power[:, 0]

        power_chan2 = power[:, 1]

        #power_chan3 = power[:, 2]

        #power_chan4 = power[:, 3]

        matDict = dict();

        matDict['wavelength'] = wavelength;

        # matDict['power'] = power[:, 0];

        matDict['power1'] = power_chan1

        matDict['power2'] = power_chan2

        savemat(baseFolder+matFilename, matDict);

        #Every n number of sweeps, do a fine align:
        if i%45 ==0 or i==1:
            fine_align_wavelength = find_optimum_wavelength(matDict,guess_wavelength=central_wavelength,range = 2e-9)
            run_fine_align(laser,Stage,optimum_wavelength=fine_align_wavelength)



    # Change power units to dBm after sweep

    laser.setAutorangeAll()

    laser.setTLSWavelength = central_wavelength;



    #%%  Debug

    detpower = laser.readPWM(1, 0);

    print "detector power is" + str(detpower)

    laser.disconnect();