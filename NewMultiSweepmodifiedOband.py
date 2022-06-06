## This was originally written by Michael Caverley in 2015
## Code has been modified by Eric Lyall in December 2020 ericlyall1428@gmail.com
## It was modified for the 8164A laser set-up at the Life Sciences Institute at UBC. The laser has 2 active detectors.
## An option for a periodic fine align is/has been added
## 2021-03-31 S. Grist added saving the timestamp associated with each sweep to a CSV.

## Import Statements:

#import hp816x_instr
#reload(hp816x_instr)
N77 = 0
if N77 == 1:
    import hp816x_Oband_N77Det_instr

    reload(hp816x_Oband_N77Det_instr)
    laser = hp816x_Oband_N77Det_instr.hp816x_Oband_N77Det();
    laser.connect('GPIB0::22::INSTR', 'TCPIP0::100.65.11.185::inst0::INSTR', reset=0, forceTrans=1)

if N77 == 0:
    import hp816x_instr

    reload(hp816x_instr)
    laser = hp816x_instr.hp816x();
    laser.connect('GPIB0::22::INSTR', reset=0, forceTrans=1)

import matplotlib.pyplot as plt
from scipy.io import savemat
import time
#from pyOptomipMaster.pyOptomip.fineAlign import fineAlign
from fineAlign import fineAlign
from CorvusEco import CorvusEcoClass
import os
import visa
import numpy as np
import time
import csv
from datetime import datetime
import sys

sys.path.append('C:/Users/MapleLeafStage/PycharmProjects/TestingPycharmMaple/Maple Setup/Maple Setup/NewMultisweep')

def calc_slice_indices (wavelength, guess_wavelength,range):
    st_index = int((guess_wavelength-range - wavelength[0])/(wavelength[len(wavelength)-1]-wavelength[0])*len(wavelength))
    end_index = int((guess_wavelength+range - wavelength[0])/(wavelength[len(wavelength)-1]-wavelength[0])*len(wavelength))
    return st_index,end_index

def find_optimum_wavelength(matdict, guess_wavelength=1310e-9,range=2e-9):
    #Trying to find a good wavelength to fine align to.
    #Do this by searching for the highest combined power readings withing +- range of a guessing wavelength
    #For example, if the guess wavelength was 1550 and rage 2, would look for the highest combined power reading from
    #1548 to 1552 nm, and then return this wavelength to do a fine alignment.

    wavelength = np.array(matdict['wavelength']) # retrieving the wavelengths used during the sweep (nm)
    power1 = np.array(matdict['power1'])        # retrieving the values for the power1 channel. (dBm)
    power2 = np.array(matdict['power2']) # retrieving the values for the power2 channel. (dBm)
    power3 = np.array(matdict['power3'])  # retrieving the values for the power1 channel. (dBm)
    power4 = np.array(matdict['power4'])  #
    power5 = np.array(matdict['power5'])  # retrieving the values for the power1 channel. (dBm)
    power6 = np.array(matdict['power6'])  #
    power7 = np.array(matdict['power7'])  # retrieving the values for the power1 channel. (dBm)
    power8 = np.array(matdict['power8'])  #
   # power9 = np.array(matdict['power9'])
    #power10 = np.array(matdict['power10'])
    #power11 = np.array(matdict['power11'])
    #power12 = np.array(matdict['power12'])
    #Finding the range (by array index) to look for max combined power
    st_index, end_index = calc_slice_indices(wavelength,guess_wavelength,range)
    #Creating an array with added power, tha only looks at the previously specified range.
    combo_power = np.add(power1,power2)[st_index:end_index]
    #combo_power = np.add(power1,power2, power3, power4, power5, power6, power7, power8, power9, power10, power11, power12)[st_index:end_index]
    #combo_power = np.add(power9, power10, power11,power12)[st_index:end_index]

    max_index = combo_power.argmax() + st_index # returns the first incidence of the maximum value.
    optimum_wavelength = wavelength[max_index]

    print(optimum_wavelength)

    return optimum_wavelength

def run_fine_align(laser, stage, optimum_wavelength=1310e-9):
    """
    Runs a fine align, moving the stage around to optimize power readings
    :param laser: A connected laser
    :param stage: A connected stage
    :param optimum_wavelength: The wavelength you would like to do the fine align around. This doesn't actually do
    anything yet, as teh fineAlign wavelength gets re-defined in the fineAlign code.
    :return:
    """
    laser.setAutorangeAll()
    if N77 == 1:
        laser.N77setAutorangeAll()
    laser.setTLSWavelength(optimum_wavelength)    #Setting the laser to optimum wavelength before alignment
    print("Did the wavelegnth change to: ", optimum_wavelength*1e9)

    Align= fineAlign(laser, stage)  #Creating a new finAlign object
    Align.wavelength = optimum_wavelength

    #Want to print out the power before fine alignment:
    detectorPriority = [0, 1, 2, 3]
    for det in detectorPriority:
        detSlot = Align.laser.pwmSlotMap[det][0]
        detChan = Align.laser.pwmSlotMap[det][1]
        power = Align.laser.readPWM(detSlot, detChan)
        print("Detector", det+1, "Before fine align Power = ", power,"\n")
    if N77==1:
        N77detectorPriority = [0, 1, 2, 3]
        for det in N77detectorPriority:
            detSlot = Align.laser.N77pwmSlotMap[det][0]
            detChan = Align.laser.N77pwmSlotMap[det][1]
            power = Align.laser.N77readPWM(detSlot, detChan)
            print("Detector", det+3, "Before fine align Power = ", power, "\n")

    #Doing the actual fine Align - this is currently automatically set to 1550
    print("Starting fine align...")
    # Align.laser.ctrlPanel.laserPanel.laserPanel.haltDetTimer()
    Align.doFineAlign()

    # Getting power after fine alignment
    for det in detectorPriority:
        detSlot = Align.laser.pwmSlotMap[det][0]
        detChan = Align.laser.pwmSlotMap[det][1]
        power = Align.laser.readPWM(detSlot, detChan)
        print("Detector", det+1, "After fine align Power = ", power,"\n")
    if N77 == 1:
        for det in N77detectorPriority:
            detSlot = Align.laser.N77pwmSlotMap[det][0]
            detChan = Align.laser.N77pwmSlotMap[det][1]
            power = Align.laser.N77readPWM(detSlot, detChan)
            print("Detector", det+3, "After fine align Power = ", power, "\n")

    return

##################################################
################### STAGE TEC ####################
##################################################
stage_temp=True;
if(stage_temp):
    # Stage TEC
    import SRS_LDC501
    reload(SRS_LDC501)
    LDC_stage = SRS_LDC501.SRS_LDC501()
    LDC_stage.connect('GPIB0::4::INSTR')#, reset=0, forceTrans=1)
    Vlimit=1.2
    Ilimit=40
    #Stage_temp=15

    # Setting sTAGE temperature range and steps for sweep
    Stage_min_temp    = 20 #21.4
    Stage_max_temp    = 30#21.7
    Stage_steps_temp  = 11# Stage_max_temp-Stage_min_temp+1
    #Stage_temp_axis   = np.linspace(Stage_min_temp,Stage_max_temp, Stage_steps_temp)
    Stage_temp_axis_increment   = np.linspace(Stage_min_temp, Stage_max_temp, Stage_steps_temp)
    Stage_temp_axis_decrement   = np.linspace(Stage_max_temp, Stage_min_temp, Stage_steps_temp)
    Stage_temp_axis    = np.concatenate([Stage_temp_axis_increment, Stage_temp_axis_decrement])

    #sinusoidal_increments    = 5*np.sin(np.linspace(0, 2*3.1415926535897932384626433, Stage_steps_temp))
    #Stage_temp_axis          = Stage_min_temp + sinusoidal_increments

    Stage_TEC_wait_time= 0
    LDC_stage.setTemperature(Stage_temp_axis[0])
    LDC_stage.tecON()
    LDC_stage.getTemperature()

## Main script running here:

if __name__ == '__main__':

    #Setting up part 1 of sweep parameters
    central_wavelength = 1308.5e-9
    sweep_range = 10e-9

    ## Connecting to the laser

   # laser = hp816x_instr.hp816x();
   # laser.connect('GPIB0::20::INSTR', reset=0, forceTrans=1) ## This is the address of the GPIB cable we are using,from NI MAX
    time.sleep(6.0)  # gives the laser some time to connect
    c = 299792458
    laser.setTLSState('on');  # turn on laser
    laser.setAutorangeAll()
    if N77 == 1:
        laser.N77setAutorangeAll()
    laser.setTLSWavelength(central_wavelength)
    laser.setPWMPowerUnit(1, 0, 'dBm')

    #Connecting to the stage for fun:
    Stage = CorvusEcoClass()
    Stage.connect(visaName='ASRL4::INSTR',rm=visa.ResourceManager(),Velocity= 5, Acceleration=500, NumberOfAxis=3)

    #laser.setAutorangeAll()
    #laser.N77setAutorangeAll()
    laser.setTLSWavelength(central_wavelength)

    #Settting the base folder- this is where sweeps will save into

    #FolderName = 'C:/Users/MapleLeafStage/Documents/Archive_2020-April_2022/2022-04-28_AIM chip_Sheri/'
    FolderName = 'C:/Users/MapleLeafStage/Documents/Sheri/2022-05-08_AIM chip/'
    measurement_time = datetime.now().strftime('%Y') + "-" + datetime.now().strftime(
        '%m') + "-" + datetime.now().strftime('%d') + "_" + datetime.now().strftime(
        '%H') + "" + datetime.now().strftime('%M') + "" + datetime.now().strftime('%S')+"/"

    try:
        os.stat(FolderName + measurement_time)
    except:
        os.mkdir(FolderName + measurement_time)

    # baseFolder = 'C:/Users/eric1/Google Drive/UBC/CBR/Vinny COVID Project/Dec9Trial2/'
    #baseFolder = 'C:/Users/MapleLeafStage/Documents/2022-04-08_Gemina-Phase-3_Trial-1/Bioassay/'
    #baseFolder = 'C:/Users/MapleLeafStage/Documents/2202-04-13_ObandCalib/2202-04-14/'
    baseFolder = FolderName + measurement_time


    ## Setting up sweep parameters:

    laser.sweepStartWvl = 1308.3e-9; #central_wavelength-sweep_range;  #Starting wavelength
    laser.sweepStopWvl = 1308.7e-9; #central_wavelength+sweep_range; #Stopping wavelength
    laser.sweepStepWvl = 0.001e-9;  # step size
    laser.sweepNumScans = 1; ## I **think** the laser can average out over 1, 2 or 3 scans.
    laser.sweepSpeed = '5nm';   # '5nm' is the only sweep speed that currently works. The laser is capable of '40nm' and '.5nm',
                               # but this software is not
    laser.sweepLaserOutput = 'highpower';
    laser.sweepPower = 10;  #Always set this to 0
    laser.sweepInitialRange = 0
    power_thru = []
    power_drop = []


    #Running an initial sweep on the laser:
    start_time = time.time()
    (wavelength, power) = laser.sweep();
    print("Sweep time = ",(time.time() - start_time) ,"seconds")  ## Take note- this is how to time things in python

    # Change power units to dBm after sweep
    laser.setAutorangeAll()
    if N77 == 1:
        laser.N77setAutorangeAll()
    # laser.setTLSWavelength = 1550e-9;

    #Getting the power channels from the sweep output

    if N77 == 0:
        power_chan1 = power[:, 0]
        power_chan2 = power[:, 1]
        power_chan3 = power[:, 2]
        power_chan4 = power[:, 3]
        power_chan5 = power[:, 4]
        power_chan6 = power[:, 5]
        power_chan7 = power[:, 6]
        power_chan8 = power[:, 7]
    if N77 == 1:
        power_chan9 = power[:, 8]  #Seems like we could have multiple channels, this could be useful for future layouts.
        power_chan10 = power[:, 9]
        power_chan11 = power[:, 10]
        power_chan12 = power[:, 11]

    #Showing a plot of the initial sweep:

    plt.figure()
    if N77 == 0:
        plt.plot(wavelength*1e9,power_chan1, 'b', label='Power1')
        plt.plot(wavelength*1e9,power_chan2, 'g', label='Power2')
        plt.plot(wavelength*1e9,power_chan3, 'r', label='Power3')
        plt.plot(wavelength*1e9,power_chan4, 'k', label='Power4')
        plt.plot(wavelength*1e9,power_chan5, 'y', label='Power5')
        plt.plot(wavelength*1e9,power_chan6, 'c', label='Power6')
        plt.plot(wavelength*1e9,power_chan7, 'm', label='Power7')
        plt.plot(wavelength*1e9,power_chan8, 'b--', label='Power8')
    if N77 == 1:
        plt.plot(wavelength*1e9,power_chan9, 'b', label = 'N77Power1')
        plt.plot(wavelength*1e9,power_chan10, 'k', label = 'N77Power2')
        plt.plot(wavelength*1e9,power_chan11, 'k--', label='N77Power3')
        plt.plot(wavelength*1e9,power_chan12, 'y--', label='N77Power4')

    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Power (dBm)')
    plt.legend()
    #plt.show()
    plt.pause(2)

    ## Getting into running multiple sweeps:

    #Choosing the number of scans to preform. This affects how long the program runs for.

    nbscan=660;

    # get the initial time
    t0 = time.time()
    stage_temp_increment_sign = 1;
    LDC_stage_measured_temp = np.zeros(nbscan+1)
    i_stage_temp=0
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

        if(LDC_stage.getTemperature()>29.5):
            stage_temp_increment_sign=-1;

        if (stage_temp):
            if (i % 60 == 0):  # and i<44): # Change the stage temperature every 1 loop iterations
                i_stage_temp = i_stage_temp + 1*stage_temp_increment_sign
                if(LDC_stage.getTemperature()>19 and LDC_stage.getTemperature()<40):
                    LDC_stage.setTemperature(Stage_temp_axis[i_stage_temp])
                    time.sleep(50.0)
            LDC_stage_measured_temp[i] = LDC_stage.getTemperature()

        # sweep laser
        (wavelength, power) = laser.sweep();

        if N77 == 0:
            power_chan1 = power[:, 0]
            power_chan2 = power[:, 1]
            power_chan3 = power[:, 2]
            power_chan4 = power[:, 3]
            power_chan5 = power[:, 4]
            power_chan6 = power[:, 5]
            power_chan7 = power[:, 6]
            power_chan8 = power[:, 7]
        if N77 == 1:
            power_chan9 = power[:, 8]
            power_chan10 = power[:, 9]
            power_chan11 = power[:, 10]
            power_chan12 = power[:, 11]

        matDict = dict();

        matDict['wavelength'] = wavelength;

        # matDict['power'] = power[:, 0];

        #matDict['power'] = power
        if N77 == 0:
            matDict['power1'] = power_chan1
            matDict['power2'] = power_chan2
            matDict['power3'] = power_chan3
            matDict['power4'] = power_chan4
            matDict['power5'] = power_chan5
            matDict['power6'] = power_chan6
            matDict['power7'] = power_chan7
            matDict['power8'] = power_chan8
        if N77 == 1:
            matDict['power9'] = power_chan9
            matDict['power10'] = power_chan10
            matDict['power11'] = power_chan11
            matDict['power12'] = power_chan12

        savemat(baseFolder+matFilename, matDict);


        #Every n number of sweeps, do a fine align:
        if i%30 == 0 or i == 1:
            fine_align_wavelength = find_optimum_wavelength(matDict,guess_wavelength=central_wavelength,range = laser.sweepStepWvl)#range=2e-9
            run_fine_align(laser,Stage,optimum_wavelength=fine_align_wavelength)
    # Change power units to dBm after sweep
    laser.setAutorangeAll()
    #laser.N77setAutorangeAll()
    laser.setTLSWavelength = central_wavelength;
    #%%  Debug
    detpower = laser.readPWM(4, 0);
    print "detector power is" + str(detpower)
    laser.disconnect();