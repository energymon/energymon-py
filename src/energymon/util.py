"""
Utilities for using an energymon.

See documentation in the native energymon.h header file for additional details.
"""
import os
from ctypes import (
    CFUNCTYPE, POINTER,
    c_int, create_string_buffer, get_errno, set_errno, pointer, sizeof
)
from .energymon import energymon

def get_energymon(lib, func_get='energymon_get_default') -> energymon:
    """
    Create an energymon and 'get' it (populate its function pointers).

    Parameters
    ----------
    lib : an energymon library loaded by ctypes (e.g., a CDLL).
    func_get : the library function name used to populate the energymon struct.

    Returns
    -------
    em: energymon

    Notes
    -----
    Assumes a standard "get" function prototype: int (get) (energymon*)
    All known instances use this prototype, but the energymon API doesn't
    actually define this.
    """
    energymon_get = CFUNCTYPE(c_int, POINTER(energymon), use_errno=True)
    energymon_get_impl = energymon_get((func_get, lib))
    em = energymon()
    set_errno(0)
    if energymon_get_impl(pointer(em)) != 0:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))
    return em

def init(em: energymon):
    """Initialize the energymon (initialize private state)."""
    if not em.finit:
        raise ValueError('\'finit\' not set - did you \'get\' the energymon?')
    set_errno(0)
    if em.finit(pointer(em)) != 0:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))

def finish(em: energymon):
    """Finish the energymon (clean up private state)."""
    if not em.ffinish:
        raise ValueError('\'ffinish\' not set - did you \'get\' the energymon?')
    set_errno(0)
    if em.ffinish(pointer(em)) != 0:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))

def get_uj(em: energymon) -> int:
    """
    Get the total energy in microjoules.

    Notes
    -----
    The energymon must be initialized.
    """
    if not em.fread:
        raise ValueError('\'fread\' not set - did you \'get\' the energymon?')
    set_errno(0)
    val = em.fread(pointer(em))
    errno = get_errno()
    if val == 0 and errno != 0:
        raise OSError(errno, os.strerror(errno))
    return val

def get_source(em: energymon, maxlen=256, encoding='UTF-8', errors='strict') -> str:
    """
    Get a human-readable description of the energy monitoring source.

    Notes
    -----
    The energymon doesn't need to be initialized.
    """
    if not em.fsource:
        raise ValueError('\'fsource\' not set - did you \'get\' the energymon?')
    name = create_string_buffer(maxlen)
    ret = em.fsource(name, sizeof(name))
    if ret is None:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))
    return name.value.decode(encoding, errors)

def get_interval_us(em: energymon) -> int:
    """
    Get the refresh interval in microseconds.

    Notes
    -----
    The energymon must be initialized.
    """
    if not em.finterval:
        raise ValueError('\'finterval\' not set - did you \'get\' the energymon?')
    val = em.finterval(pointer(em))
    if val == 0:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))
    return val

def get_precision_uj(em: energymon) -> int:
    """
    Get the best possible possible read precision in microjoules.

    Notes
    -----
    The energymon must be initialized.
    """
    if not em.fprecision:
        raise ValueError('\'fprecision\' not set - did you \'get\' the energymon?')
    set_errno(0)
    val = em.fprecision(pointer(em))
    errno = get_errno()
    if val == 0 and errno != 0:
        raise OSError(errno, os.strerror(errno))
    return val

def is_exclusive(em: energymon) -> bool:
    """
    Get whether the implementation requires exclusive access.

    Notes
    -----
    The energymon must be initialized.
    """
    if not em.fexclusive:
        raise ValueError('\'fexclusive\' not set - did you \'get\' the energymon?')
    if em.fexclusive(pointer(em)) == 0:
        return False
    return True
