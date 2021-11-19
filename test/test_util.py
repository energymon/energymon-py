# pylint: disable=C0114, C0116
import ctypes
import unittest
from energymon import energymon, util

def load_default_lib():
    """
    Requires library to be discoverable, e.g., on LD_LIBRARY_PATH (POSIX systems) or
    DYLD_LIBRARY_PATH (OSX systems).
    """
    return util.load_energymon_library()


class TestEnergymonUtil(unittest.TestCase):
    """Test energymon util functions."""

    def test_load_energymon_library(self):
        self.assertIsInstance(util.load_energymon_library(), ctypes.CDLL)

    def test_load_energymon_library_bad(self):
        with self.assertRaises(FileNotFoundError):
            util.load_energymon_library('!@#$%^&*()')

    def test_get_energymon(self):
        enm = util.get_energymon(load_default_lib())
        self.assertIsInstance(enm, energymon)
        # TODO: how to test functions are set - currently always should CFUNCTYPE before/after get

    def test_init_finish(self):
        enm = util.get_energymon(load_default_lib())
        self.assertIsNone(util.init(enm))
        self.assertIsNone(util.finish(enm))

    def test_get_uj(self):
        enm = util.get_energymon(load_default_lib())
        util.init(enm)
        ret = util.get_uj(enm)
        self.assertIsInstance(ret, int)
        self.assertTrue(ret >= 0)
        util.finish(enm)

    def test_source(self):
        enm = util.get_energymon(load_default_lib())
        util.init(enm)
        ret = util.get_source(enm)
        self.assertIsInstance(ret, str)
        util.finish(enm)

    def test_interval_us(self):
        enm = util.get_energymon(load_default_lib())
        util.init(enm)
        ret = util.get_interval_us(enm)
        self.assertIsInstance(ret, int)
        self.assertTrue(ret >= 0)
        util.finish(enm)

    def test_precision_uj(self):
        enm = util.get_energymon(load_default_lib())
        util.init(enm)
        ret = util.get_precision_uj(enm)
        self.assertIsInstance(ret, int)
        self.assertTrue(ret >= 0)
        util.finish(enm)

    def test_is_exclusive(self):
        enm = util.get_energymon(load_default_lib())
        util.init(enm)
        ret = util.is_exclusive(enm)
        self.assertIsInstance(ret, bool)
        util.finish(enm)


if __name__ == '__main__':
    unittest.main()
