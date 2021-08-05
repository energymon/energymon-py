"""Bindings for energymon.h"""
from ctypes import (
    CFUNCTYPE, POINTER,
    Structure,
    c_char_p, c_int, c_size_t, c_ulonglong, c_void_p
)

class energymon(Structure):
    """Binding to energymon struct."""

energymon_init = CFUNCTYPE(c_int, POINTER(energymon), use_errno=True)
energymon_read_total = CFUNCTYPE(c_ulonglong, POINTER(energymon), use_errno=True)
energymon_finish = CFUNCTYPE(c_int, POINTER(energymon), use_errno=True)
energymon_get_source = CFUNCTYPE(c_char_p, c_char_p, c_size_t, use_errno=True)
energymon_get_interval = CFUNCTYPE(c_ulonglong, POINTER(energymon), use_errno=True)
energymon_get_precision = CFUNCTYPE(c_ulonglong, POINTER(energymon), use_errno=True)
energymon_is_exclusive = CFUNCTYPE(c_int, use_errno=True)

energymon._fields_ = [
    ('finit', energymon_init),
    ('fread', energymon_read_total),
    ('ffinish', energymon_finish),
    ('fsource', energymon_get_source),
    ('finterval', energymon_get_interval),
    ('fprecision', energymon_get_precision),
    ('fexclusive', energymon_is_exclusive),
    ('state', c_void_p)
]
