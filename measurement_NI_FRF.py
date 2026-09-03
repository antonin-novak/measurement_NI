
import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from functions.SynchSweptSine import SynchSweptSine


""" Parameters """
Dev = 'Dev4'        # name of the NI device
fs = 48000          # sampling frequency [Hz]
mic_sens = 49.8e-3  # V/Pa

""" Generate a Swept-sine signal"""
f1 = 20                     # start frequency [Hz]
f2 = 20e3                   # end frequency [Hz]
T = 5                       # time length of the swept-sine [s]

# note that 'sss' is an object.
sss = SynchSweptSine(f1=f1, f2=f2, T=T, fs=fs)
out_signal = np.concatenate((sss.signal, np.zeros(int(0.5*fs))))

""" Measurement using a National Instruments device  """
y = measurement_NI(out_signal, fs, Dev, iepe=[False])

# Extract signals from measured data (voltage)
p = np.array(y) / mic_sens  # convert to pressure [Pa]

P = sss.get_FRF(p)
f_axis = sss.f_axis(len(p))

""" Plot the results """
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(P/2e-5/np.sqrt(2))))
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude')
ax.set_title('Frequency Response Function')
ax.grid(True)

plt.show()
