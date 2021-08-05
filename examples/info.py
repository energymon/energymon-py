"""Example similar to the energymon-info utility."""
from ctypes import (
    CDLL, CFUNCTYPE, POINTER,
    c_int, create_string_buffer, get_errno, pointer, sizeof
)
from ctypes.util import find_library
from energymon import energymon
import errno
import os
import sys

def get_energymon():
    """
    Get an energymon instance.

    Assumes a standard "get" function prototype, but this is not actually
    enforced by the energymon API.
    All known instances uses this prototype, but it is not strictly required.
    """
    lib_name = "energymon-default"
    fn_get_name = "energymon_get_default"
    energymon_get = CFUNCTYPE(c_int, POINTER(energymon), use_errno=True)
    if len(sys.argv) > 1:
        lib_name = sys.argv[1]
    if len(sys.argv) > 2:
        fn_get_name = sys.argv[2]
    lib = CDLL(find_library(lib_name), use_errno=True)
    energymon_get_impl = energymon_get((fn_get_name, lib))
    em = energymon()
    rc = energymon_get_impl(pointer(em))
    if rc != 0:
        print(f'{fn_get_name}: {os.strerror(get_errno())}')
        exit(rc)
    return em

em = get_energymon()
pem = pointer(em)
# A simpler approach if you know the library and function names in advance:
# lib = CDLL("libenergymon-default.so", use_errno=True)
# em = energymon()
# pem = pointer(em)
# rc = lib.energymon_get_default(pem)
# ...

name = create_string_buffer(256)
em.fsource(name, sizeof(name))
print('source:', repr(name.value))

rc = em.finit(pem)
if rc != 0:
    print('energymon:finit:', os.strerror(get_errno()))
    exit(rc)

exclusive = em.fexclusive(pem)
print('exclusive:', exclusive)

interval = em.finterval(pem)
print('interval (usec):', interval)

precision = em.fprecision(pem)
print('precision (uJ):', precision)

uj = em.fread(pem)
if uj == 0 and get_errno() != 0:
    print('fread:', os.strerror(get_errno()))
else:
    print('reading (uJ):', uj)

rc = em.ffinish(pem)
if rc != 0:
    print('energymon:ffinish:', os.strerror(get_errno()))
    exit(rc)
