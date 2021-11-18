# pylint: disable=C0114, C0116
import unittest
from ctypes import CDLL, byref, create_string_buffer, sizeof
from ctypes.util import find_library
from energymon import energymon

def load_default_lib():
    """
    Requires library to be discoverable, e.g., on LD_LIBRARY_PATH (POSIX systems) or
    DYLD_LIBRARY_PATH (OSX systems).
    """
    lib_path = find_library('energymon-default')
    return CDLL(lib_path, use_errno=True)


class TestEnergymon(unittest.TestCase):
    """Test energymon struct bindings."""

    def get_default_energymon(self):
        lib = load_default_lib()
        enm = energymon()
        # TODO: Be able to set and check NULL values on function pointers, then test them
        self.assertEqual(lib.energymon_get_default(byref(enm)), 0)
        return enm

    def test_get_default_energymon(self):
        self.assertIsInstance(self.get_default_energymon(), energymon)

    def test_default_lifecycle(self):
        enm = self.get_default_energymon()
        self.assertEqual(enm.finit(byref(enm)), 0)
        self.assertEqual(enm.ffinish(byref(enm)), 0)

    def test_getters(self):
        enm = self.get_default_energymon()
        ptr = byref(enm)
        self.assertEqual(enm.finit(ptr), 0)
        self.assertTrue(enm.fread(ptr) >= 0)
        name = create_string_buffer(256)
        self.assertIsNotNone(enm.fsource(name, sizeof(name)))
        self.assertTrue(enm.finterval(ptr) >= 0)
        self.assertTrue(enm.fprecision(ptr) >= 0)
        self.assertTrue(enm.fexclusive() >= 0)
        self.assertEqual(enm.ffinish(ptr), 0)


if __name__ == '__main__':
    unittest.main()
