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
    Create an energymon and 'get' it (populate its function pointers), but do
    not initialize it.

    Parameters
    ----------
    lib : ctypes library
        An energymon library loaded by ctypes (e.g., a CDLL).
    func_get : str
        The library function name used to populate the energymon struct.

    Returns
    -------
    energymon
        An uninitialized energymon instance.

    Raises
    ------
    AttributeError
        If the getter function is not found.
    OSError
        If the underlying function returns an error.
        This is allowed by the API but should not occur under normal conditions.

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
    """
    Initialize the energymon (initialize private state).

    Parameters
    ----------
    em : energymon
        The energymon must not be initialized.

    Raises
    ------
    OSError
        If the underlying function returns an error.
        This may occur under normal conditions, e.g., if the sensors are not
        present or cannot be initialized.
    """
    if not em.finit:
        raise ValueError('\'finit\' not set - did you \'get\' the energymon?')
    set_errno(0)
    if em.finit(pointer(em)) != 0:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))

def finish(em: energymon):
    """
    Finish the energymon (clean up private state).

    Parameters
    ----------
    em : energymon
        The energymon must be initialized.

    Raises
    ------
    OSError
        If the underlying function returns an error.
        This may occur under normal conditions, but is unlikely.
    """
    if not em.ffinish:
        raise ValueError('\'ffinish\' not set - did you \'get\' the energymon?')
    set_errno(0)
    if em.ffinish(pointer(em)) != 0:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))

def get_uj(em: energymon) -> int:
    """
    Get the total energy in microjoules.

    Parameters
    ----------
    em : energymon
        The energymon must be initialized.

    Returns
    -------
    int
        The total energy in microjoules.

    Raises
    ------
    OSError
        If the underlying function returns an error.
        This may occur under normal conditions for some underlying sensors.
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

    Parameters
    ----------
    em : energymon
        The energymon doesn't need to be initialized.

    Returns
    -------
    str
        A human-readable description of the energy monitoring source.

    Raises
    ------
    OSError
        If the underlying function returns an error.
        This is allowed by the API but should not occur under normal conditions.
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

    Parameters
    ----------
    em : energymon
        The energymon must be initialized.

    Returns
    -------
    int
        The refresh interval in microseconds.
        This value should be greater than 0.
        If there is no minimum interval, returns 1.

    Raises
    ------
    OSError
        If the underlying function returns an error.
        This is allowed by the API but should not occur under normal conditions.
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

    For implementations that read from power sensors, this is a function of
    the precision of the power readings and the refresh interval.

    Parameters
    ----------
    em : energymon
        The energymon must be initialized.

    Returns
    -------
    int
        The best possible possible read precision in microjoules.
        If 0 < precision <= 1, returns 1.
        If the precision is unknown, returns 0.

    Raises
    ------
    OSError
        If the underlying function returns an error.
        This is allowed by the API but should not occur under normal conditions.
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

    In such cases it may be beneficial to run in a separate process and expose
    energy data over shared memory (or other means) so multiple applications can
    use the data source simultaneously.

    Parameters
    ----------
    em : energymon
        The energymon doesn't need to be initialized.

    Returns
    -------
    bool
        True if the implementation requires exclusive access, False otherwise.
    """
    if not em.fexclusive:
        raise ValueError('\'fexclusive\' not set - did you \'get\' the energymon?')
    return bool(em.fexclusive())
