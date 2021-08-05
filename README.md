# EnergyMon Python Bindings

This project provides Python bindings to energymon libraries.

If using this project for other scientific works or publications, please reference:

* Connor Imes, Lars Bergstrom, and Henry Hoffmann. "A Portable Interface for Runtime Energy Monitoring". In: FSE. 2016. DOI: https://doi.org/10.1145/2950290.2983956


## Dependencies

The `energymon` libraries should be installed to the system and on the library search path (e.g., `LD_LIBRARY_PATH`).

The latest `energymon` C libraries can be found at https://github.com/energymon/energymon.


## Building

To install from source:

```sh
pip install .
```


## Usage

The module exposes an `energymon` class, which is a binding to the `energymon` C struct.
Users can load an energymon library and "get" the struct to populate its function pointers.
For example:

```Python
from ctypes import CDLL, pointer
from energymon import energymon

lib = CDLL("libenergymon-default.so", use_errno=True)
em = energymon()
pem = pointer(em)

if lib.energymon_get_default(pem) != 0:
    # handle failure...
```

Then initialize, do work like get readings, and cleanup when finished:

```Python
if em.finit(pem) != 0:
    # handle failure...
uj_start = em.fread(pem)
# do work...
uj_end = em.fread(pem)
# do something with readings...
if em.ffinish(pem) != 0:
    # handle failure...
```


## Project Source

Find this and related project sources at the [energymon organization on GitHub](https://github.com/energymon).  
This project originates at: https://github.com/energymon/energymon-py

Bug reports and pull requests for bug fixes and enhancements are welcome.
