# LSI pyOptomip

## Requirements

* Windows
* [816x VXI Plug&Play Driver](https://www.keysight.com/ca/en/lib/software-detail/driver/816x-vxi-plugplay-driver-112417.html)
* Python3.7~3.9 (3.9 preferred)

## Installation

1. Clone this folder to your local drive
2. ```python -m venv .venv```
3. ```pip install -r requirements.txt```

## Usage
### pyOptomip
```
pythonw pyOptomip.pyw
```
#### Connect to Instruments
TODO:
#### Laser Control
TODO:
#### Run Sweep
TODO:
#### Stage Control
TODO:
#### Fine-Align
TODO:

### Multi-Sweep
```toml
# multi-sweep.toml
# Sample multi-sweep configuration file, make sure this exists in the same folder with multi-sweep.py

name = "experiment-1"                # unused for now
base-folder = "~/path/to/experiment" # folder to save the results
number-of-scans = 5000               # this affects how long the program runs for.
[laser]
with-n77 = true
is-oband = false
[range]
start = 1520e-9 # sweeping start wavelength
stop = 1570e-9  # sweeping stop wavelength
[fine-align]
frequency = 30 # fine align per {frequency} sweeps
```

```
python multi-sweep.py
```

The first result will pop up. Close that window to continue. The remaining sweep results will be saved without showing a window.

Press `Ctrl+C` in the terminal to force stop.