## This was originally written by Michael Caverley in 2015
## Code has been modified by Eric Lyall in December 2020 ericlyall1428@gmail.com
## It was modified for the 8164A laser set-up at the Life Sciences Institute at UBC. The laser has 2 active detectors.
## An option for a periodic fine align is/has been added
## 2021-03-31 S. Grist added saving the timestamp associated with each sweep to a CSV.

from typing import Optional, Union

import os
import time
import csv
import toml

import pyvisa as visa
import numpy as np

from matplotlib import pyplot as plt
from scipy.io import savemat

from hp816x_instr import hp816x
from hp816x_N77Det_instr import hp816x_N77Det
from fineAlign import fineAlign
from CorvusEco import CorvusEcoClass


def calc_slice_indices(wavelength, guess_wavelength, range):
    st_index = int(
        (guess_wavelength - range - wavelength[0])
        / (wavelength[len(wavelength) - 1] - wavelength[0])
        * len(wavelength)
    )
    end_index = int(
        (guess_wavelength + range - wavelength[0])
        / (wavelength[len(wavelength) - 1] - wavelength[0])
        * len(wavelength)
    )
    return st_index, end_index


def find_optimum_wavelength(matdict, guess_wavelength=1560e-9, range=2e-9):
    # Trying to find a good wavelength to fine align to.
    # Do this by searching for the highest combined power readings withing +- range of a guessing wavelength
    # For example, if the guess wavelength was 1550 and rage 2, would look for the highest combined power reading from
    # 1548 to 1552 nm, and then return this wavelength to do a fine alignment.

    wavelength = np.array(
        matdict["wavelength"]
    )  # retrieving the wavelengths used during the sweep (nm)
    power1 = np.array(
        matdict["power1"]
    )  # retrieving the values for the power1 channel. (dBm)
    power2 = np.array(
        matdict["power2"]
    )  # retrieving the values for the power2 channel. (dBm)
    # Finding the range (by array index) to look for max combined power
    st_index, end_index = calc_slice_indices(wavelength, guess_wavelength, range)
    # Creating an array with added power, tha only looks at the previously specified range.
    combo_power = np.add(power1, power2)[st_index:end_index]

    max_index = (
        combo_power.argmax() + st_index
    )  # returns the first incidence of the maximum value.

    optimum_wavelength = wavelength[max_index]

    print(optimum_wavelength)

    return optimum_wavelength


def run_fine_align(laser, stage, optimum_wavelength=1560e-9):
    """
    Runs a fine align, moving the stage around to optimize power readings
    :param laser: A connected laser
    :param stage: A connected stage
    :param optimum_wavelength: The wavelength you would like to do the fine align around. This doesn't actually do
    anything yet, as teh fineAlign wavelength gets re-defined in the fineAlign code.
    :return:
    """
    laser.setAutorangeAll()
    laser.N77setAutorangeAll()
    laser.setTLSWavelength(
        optimum_wavelength
    )  # Setting the laser to optimum wavelength before alignment
    print("Did the wavelegnth change to: ", optimum_wavelength * 1e9)

    Align = fineAlign(laser, stage)  # Creating a new finAlign object
    Align.wavelength = optimum_wavelength

    # Want to print out the power before fine alignment:
    detectorPriority = [0, 1]
    for det in detectorPriority:
        detSlot = Align.laser.pwmSlotMap[det][0]
        detChan = Align.laser.pwmSlotMap[det][1]
        power = Align.laser.readPWM(detSlot, detChan)
        print("Detector", det + 1, "Before fine align Power = ", power, "\n")
    if is_N77 == 1:
        N77detectorPriority = [0, 1, 2, 3]
        for det in N77detectorPriority:
            detSlot = Align.laser.N77pwmSlotMap[det][0]
            detChan = Align.laser.N77pwmSlotMap[det][1]
            power = Align.laser.N77readPWM(detSlot, detChan)
            print("Detector", det + 3, "Before fine align Power = ", power, "\n")

    # Doing the actual fine Align - this is currently automatically set to 1550
    print("Starting fine align...")
    # Align.laser.ctrlPanel.laserPanel.laserPanel.haltDetTimer()
    Align.doFineAlign()

    # Getting power after fine alignment
    for det in detectorPriority:
        detSlot = Align.laser.pwmSlotMap[det][0]
        detChan = Align.laser.pwmSlotMap[det][1]
        power = Align.laser.readPWM(detSlot, detChan)
        print("Detector", det + 1, "After fine align Power = ", power, "\n")
    if is_N77 == 1:
        for det in N77detectorPriority:
            detSlot = Align.laser.N77pwmSlotMap[det][0]
            detChan = Align.laser.N77pwmSlotMap[det][1]
            power = Align.laser.N77readPWM(detSlot, detChan)
            print("Detector", det + 3, "After fine align Power = ", power, "\n")

    return


## Main script running here:

if __name__ == "__main__":
    # read configuration file
    config = toml.load("multi-sweep.toml")

    name = str(config["name"])
    baseFolder = os.path.expanduser(str(config["base-folder"]))
    start_wl = float(config["range"]["start"])
    stop_wl = float(config["range"]["stop"])
    fa_freq = int(config["fine-align"]["frequency"])
    is_N77 = bool(config["laser"]["with-n77"])
    is_OBand = bool(config["laser"]["is-oband"])
    # Choosing the number of scans to preform. This affects how long the program runs for.
    nbscan = config["number-of-scans"]

    if not os.path.exists(baseFolder):
        os.makedirs(baseFolder)

    laser: Optional[Union[hp816x, hp816x_N77Det]] = None
    if is_N77:
        laser = hp816x_N77Det()
        if is_OBand:
            laser.connect(
                "GPIB0::22::INSTR",
                "TCPIP0::100.65.11.185::inst0::INSTR",
                reset=0,
                forceTrans=1,
            )  # OBand
        else:
            laser.connect(
                "GPIB0::20::INSTR",
                "TCPIP0::100.65.11.185::inst0::INSTR",
                reset=0,
                forceTrans=1,
            )  # CBand
    else:
        laser = hp816x()
        laser.connect("GPIB0::20::INSTR", reset=0, forceTrans=1)  # CBand

    # Setting up part 1 of sweep parameters
    central_wavelength = (start_wl + stop_wl) / 2
    sweep_range = (stop_wl - start_wl) / 2

    ## Connecting to the laser

    time.sleep(6.0)  # gives the laser some time to connece
    laser.setTLSState("on")
    # turn on laser
    laser.setAutorangeAll()
    laser.N77setAutorangeAll()
    laser.setTLSWavelength(central_wavelength)
    laser.setPWMPowerUnit(1, 0, "dBm")

    # Connecting to the stage for fun:
    Stage = CorvusEcoClass()
    Stage.connect(
        visaName="ASRL4::INSTR",
        rm=visa.ResourceManager(),
        Velocity=5,
        Acceleration=500,
        NumberOfAxis=3,
    )

    laser.setAutorangeAll()
    laser.N77setAutorangeAll()
    laser.setTLSWavelength(central_wavelength)

    ## Setting up sweep parameters:

    laser.sweepStartWvl = central_wavelength - sweep_range
    # Starting wavelength
    laser.sweepStopWvl = central_wavelength + sweep_range
    # Stopping wavelength
    laser.sweepStepWvl = 8e-12
    # step size
    laser.sweepNumScans = 1
    ## I **think** the laser can average out over 1, 2 or 3 scans.
    laser.sweepSpeed = "5nm"
    # '5nm' is the only sweep speed that currently works. The laser is capable of '40nm' and '.5nm',
    # but this software is not
    laser.sweepLaserOutput = "highpower"
    laser.sweepPower = 0
    # Always set this to 0
    laser.sweepInitialRange = -20
    power_thru = []
    power_drop = []

    # Running an initial sweep on the laser:
    start_time = time.time()
    (wavelength, power) = laser.sweep()
    print(
        "Sweep time = ", (time.time() - start_time), "seconds"
    )  ## Take note- this is how to time things in python

    # Change power units to dBm after sweep
    laser.setAutorangeAll()
    laser.N77setAutorangeAll()

    # Getting the power channels from the sweep output

    power_chan1 = power[:, 0]
    power_chan2 = power[:, 1]
    if is_N77:
        power_chan3 = power[
            :, 2
        ]  # Seems like we could have multiple channels, this could be useful for future layouts.
        power_chan4 = power[:, 3]
        power_chan5 = power[:, 4]
        power_chan6 = power[:, 5]
        power_chan7 = power[:, 6]
        power_chan8 = power[:, 7]
        if is_OBand:
            power_chan9 = power[:, 8]
            power_chan10 = power[:, 9]

    # Showing a plot of the initial sweep:

    plt.figure()
    plt.plot(wavelength * 1e9, power_chan1, "r", label="Power1")
    plt.plot(wavelength * 1e9, power_chan2, "g", label="Power2")
    if is_N77 == 1:
        plt.plot(wavelength * 1e9, power_chan3, "b", label="Power3")
        plt.plot(wavelength * 1e9, power_chan4, "c", label="Power4")
        plt.plot(wavelength * 1e9, power_chan5, "m", label="Power5")
        plt.plot(wavelength * 1e9, power_chan6, "y", label="Power6")
        plt.plot(wavelength * 1e9, power_chan7, "k", label="Power7")
        plt.plot(wavelength * 1e9, power_chan8, "r", label="Power8")
        if is_OBand == 1:
            plt.plot(wavelength * 1e9, power_chan9, "g", label="Power9")
            plt.plot(wavelength * 1e9, power_chan10, "b", label="Power10")

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Power (dBm)")
    plt.legend()
    plt.show()

    ## Getting into running multiple sweeps:

    # get the initial time
    t0 = time.time()

    for i in range(1, nbscan + 1):
        # get elapsed time
        t1 = time.time()
        t_elapse = t1 - t0

        matFilename = "laser_sweep_%d.mat" % i

        # save elapsed time to CSV
        csvFilename = "timeSteps.csv"
        with open(os.path.join(baseFolder, csvFilename), "a") as f:
            writer = csv.writer(f)
            writer.writerow([i, matFilename, t_elapse])

        # sweep laser

        (wavelength, power) = laser.sweep()

        power_chan1 = power[:, 0]
        power_chan2 = power[:, 1]
        if is_N77 == 1:
            power_chan3 = power[:, 2]
            power_chan4 = power[:, 3]
            power_chan5 = power[:, 4]
            power_chan6 = power[:, 5]
            power_chan7 = power[:, 6]
            power_chan8 = power[:, 7]
            if is_OBand == 1:
                power_chan9 = power[:, 8]
                power_chan10 = power[:, 9]

        matDict = dict()

        matDict["wavelength"] = wavelength

        matDict["power"] = power
        matDict["power1"] = power_chan1
        matDict["power2"] = power_chan2
        if is_N77 == 1:
            matDict["power3"] = power_chan3
            matDict["power4"] = power_chan4
            matDict["power5"] = power_chan5
            matDict["power6"] = power_chan6
            matDict["power7"] = power_chan7
            matDict["power8"] = power_chan8
            if is_OBand == 1:
                matDict["power9"] = power_chan9
                matDict["power10"] = power_chan10

        savemat(os.path.join(baseFolder, matFilename), matDict)

        # Every n number of sweeps, do a fine align:
        if i % fa_freq == 0 or i == 1:
            fine_align_wavelength = find_optimum_wavelength(
                matDict, guess_wavelength=central_wavelength, range=2e-9
            )
            run_fine_align(laser, Stage, optimum_wavelength=fine_align_wavelength)

    laser.setAutorangeAll()
    laser.N77setAutorangeAll()
    laser.setTLSWavelength(central_wavelength)
    #%%  Debug
    detpower = laser.readPWM(4, 0)
    print("detector power is" + str(detpower))
    laser.disconnect()
