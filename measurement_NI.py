# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import AcquisitionType, TaskMode


def measurement_NI(x, fs, Dev):
    ''' Measurement using National Instruments (NI) devices

    Description:
        The function creates a task that communicates with a NI 'Dev' device.
        It is designed to work with devices with 1 output and 4 inputs (e.g. NI-USB-4431).
        Sensitivities are not included, they must be considered separately.

    Usage: 
        y = measurement_NI(x, fs, Dev)
        #  Inputs:
        #    x   ... inputs signal
        #    fs  ... sample rate
        #    Dev ... name of the NI device (e.g. 'Dev1')
        #  Output:
        #    y   ... containes 4 channels of len(x) samples

    Author:
        Antonin Novak - 06.02.2025

    Version:
        1.0

    '''

    with nidaqmx.Task() as master_task, nidaqmx.Task() as slave_task:
        master_task.ao_channels.add_ao_voltage_chan(
            Dev + "/ao0", min_val=-3.5, max_val=3.5)  # analog output port is reserved
        slave_task.ai_channels.add_ai_voltage_chan(
            Dev + "/ai0")  # analog input port is reserved
        slave_task.ai_channels.add_ai_voltage_chan(
            Dev + "/ai1")  # analog input port is reserved
        slave_task.ai_channels.add_ai_voltage_chan(
            Dev + "/ai2")  # analog input port is reserved
        slave_task.ai_channels.add_ai_voltage_chan(
            Dev + "/ai3")  # analog input port is reserved

        # analog input port is configured for continuous 8000 s/s )
        master_task.timing.cfg_samp_clk_timing(
            fs, sample_mode=AcquisitionType.CONTINUOUS)
        # analog output port is configured for continous 8000 s/S
        slave_task.timing.cfg_samp_clk_timing(
            fs, sample_mode=AcquisitionType.CONTINUOUS)

        """ Done """

        """ Start generating AO and reading AI"""

        master_task.write(x)  # analog output buffer is filled with sine wave
        # analog output port is committed
        master_task.control(TaskMode.TASK_COMMIT)

        # analog input port is committed
        slave_task.control(TaskMode.TASK_COMMIT)

        print('Acqusition is started')
        slave_task.start()
        master_task.start()

        """ Done """

        result = slave_task.read(
            number_of_samples_per_channel=len(x), timeout=-1)  # analog input

        print('Acqusition is finished')
        return result


if __name__ == "__main__":
    '''
    Example:
        This script demonstrates how to generate a sinusoidal signal using a National Instruments (NI) data acquisition device,
        record the inputs, and plot the results. The script creates a sine wave signal, sends it to the NI device's output channel,
        and reads the response from the input channels. The recorded data is then plotted using matplotlib.
        The main steps are:
        1. Define the sampling frequency, signal frequency, and duration.
        2. Set the device name (e.g. 'Dev3').
        3. Generate a sine wave signal.
        4. Call the `measurement_NI` function to send the signal to the NI device and read the input channels.
        5. Plot the recorded input signals.
    '''

    """ Creating Sine wave for Analog output generation"""

    fs = 48000  # sampling frequency
    f0 = 50  # frequency of signal
    T = 1  # time duration
    t = np.arange(0, T, 1/fs)  # time domain array
    x = np.sin(2 * np.pi * f0 * t)  # sine wave

    """ Done """

    y = measurement_NI(x, fs, 'Dev3')
    u = y[0]
    i = y[1]

    fig, ax = plt.subplots(2)
    ax[0].plot(t, u)
    ax[1].plot(t, i)
