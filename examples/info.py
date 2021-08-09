"""Example similar to the energymon-info utility."""
from ctypes import CDLL
from ctypes.util import find_library
from energymon import energymon, util
import sys

lib_name = "energymon-default"
fn_get_name = "energymon_get_default"
if len(sys.argv) > 1:
    lib_name = sys.argv[1]
if len(sys.argv) > 2:
    fn_get_name = sys.argv[2]

lib = CDLL(find_library(lib_name), use_errno=True)
em = util.get_energymon(lib, fn_get_name)
print('source:', util.get_source(em))
util.init(em)
try:
    print('exclusive:', util.is_exclusive(em))
    print('interval (usec):', util.get_interval_us(em))
    print('precision (uJ):', util.get_precision_uj(em))
    print('reading (uJ):', util.get_uj(em))
finally:
    util.finish(em)
