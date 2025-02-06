## Overview
This project provides a Python script for performing data acquisition using National Instruments (NI) devices. The script generates a signal, sends it to the NI device's output channel, and simultaneously reads responses from multiple input channels.

## Features
- Communicates with NI devices using the `nidaqmx` library
- Supports continuous sampling at a specified sample rate
- Outputs a signal through the analog output channel
- Records responses from up to four analog input channels

## Requirements
### Hardware
- National Instruments device (e.g., NI-USB-4431)
  - 1 analog output channel
  - 4 analog input channels

### Software
- Python 3.x
- Libraries:
  - numpy
  - matplotlib
  - nidaqmx

## Installation
 
You can install the `nidaqmx` from from PyPI:  
```sh  
python -m pip install nidaqmx 
```

(for more details see [https://nidaqmx-python.readthedocs.io/en/stable/](https://nidaqmx-python.readthedocs.io/en/stable/)



## Usage
### Function measurement_NI():
Configures NI device for data acquisition, outputs a signal, and records channel responses.

#### Parameters:
- `x`: Input signal 
- `fs`: Sampling frequency (Hz)
- `Dev`: NI device name (e.g., 'Dev3')

#### Example

```python
fs = 48000  # Sampling frequency
f0 = 50     # Signal frequency
T = 1       # Duration

t = np.arange(0, T, 1/fs)
x = np.sin(2 * np.pi * f0 * t)
y = measurement_NI(x, fs, ‘Dev3’)
```


## Notes
- Sensitivities must be handled separately
- Ensure device compatibility with continuous sampling


## Author
 
Antonin Novak, Le Mans University, FRANCE

## License
 
This project is licensed under the MIT License.
