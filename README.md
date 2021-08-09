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
First, users are responsible for loading an energymon library using ctypes.
For example:

```Python
from ctypes import CDLL
from ctypes.util import find_library

# maybe try to find the library by name:
lib_path = find_library("energymon-default")
if lib_path is None:
    # maybe fall back on a relative or absolute path
    lib_path = "libenergymon-default.so"
lib = CDLL(lib_path, use_errno=True)
```

The module exposes some utilities to simplify usage, e.g., to "get" the energymon, handle pointers, convert data types, check for errors, and raise exceptions.
For example:

```Python
from energymon import util

em = util.get_energymon(lib, 'energymon_get_default')
print(util.get_source(em))
util.init(em)
try:
    print(util.get_uj(em))
finally:
    util.finish(em)
```


### Direct bindings

To directly use the energymon API, create and "get" the struct to populate its function pointers, then initialize, do work, and cleanup when finished.
For example:

```Python
from ctypes import pointer, create_string_buffer, sizeof, set_errno, get_errno
from energymon import energymon

em = energymon()
pem = pointer(em)

if lib.energymon_get_default(pem) != 0:
    # handle error...
    exit(1)

name = create_string_buffer(256)
if not em.fsource(name, sizeof(name)):
    # handle error
    exit(1)

print(name.value.decode())
if em.finit(pem) != 0:
    # handle error
    exit(1)

set_errno(0)
uj = em.fread(pem)
if uj == 0 and get_errno() != 0:
    # handle error (but don't skip cleanup!)
    pass

if em.ffinish(pem) != 0:
    # handle error
    exit(1)
```


## Project Source

Find this and related project sources at the [energymon organization on GitHub](https://github.com/energymon).  
This project originates at: https://github.com/energymon/energymon-py

Bug reports and pull requests for bug fixes and enhancements are welcome.
