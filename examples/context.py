# pylint: disable=C0103
"""Example similar to the energymon-info utility."""
import sys
from energymon.context import EnergyMon

def run():
    """Print energymon info."""
    lib_name = "energymon-default"
    fn_get_name = "energymon_get_default"
    if len(sys.argv) > 1:
        lib_name = sys.argv[1]
    if len(sys.argv) > 2:
        fn_get_name = sys.argv[2]

    em = EnergyMon(lib=lib_name, func_get=fn_get_name)
    print('source:', em.get_source())
    print('exclusive:', em.is_exclusive())
    with em:
        print('interval (usec):', em.get_interval_us())
        print('precision (uJ):', em.get_precision_uj())
        print('reading (uJ):', em.get_uj())


if __name__ == '__main__':
    run()
