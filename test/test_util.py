# pylint: disable=C0114, C0116
import ctypes
import unittest
from energymon import energymon, util

class TestEnergymonUtil(unittest.TestCase):
    """Test energymon util functions."""

    def test_load_energymon_library(self):
        self.assertIsInstance(util.load_energymon_library(), ctypes.CDLL)

    def test_load_energymon_library_bad(self):
        with self.assertRaises(FileNotFoundError):
            util.load_energymon_library('!@#$%^&*()')

    def test_get_energymon(self):
        enm = util.get_energymon(util.load_energymon_library())
        self.assertIsInstance(enm, energymon)
        for fptr in [enm.finit, enm.fread, enm.ffinish, enm.fsource, enm.finterval, enm.fprecision,
                     enm.fexclusive]:
            self.assertTrue(fptr)

    def test_init_finish(self):
        enm = util.get_energymon(util.load_energymon_library())
        self.assertIsNone(util.init(enm))
        self.assertIsNone(util.finish(enm))

    def test_init_unget(self):
        enm = energymon()
        with self.assertRaises(ValueError):
            util.init(enm)

    def test_finish_unget(self):
        enm = energymon()
        with self.assertRaises(ValueError):
            util.finish(enm)

    def test_get_uj(self):
        enm = util.get_energymon(util.load_energymon_library())
        util.init(enm)
        ret = util.get_uj(enm)
        self.assertIsInstance(ret, int)
        self.assertTrue(ret >= 0)
        util.finish(enm)

    def test_get_uj_unget(self):
        enm = energymon()
        with self.assertRaises(ValueError):
            util.get_uj(enm)

    def test_source(self):
        enm = util.get_energymon(util.load_energymon_library())
        util.init(enm)
        ret = util.get_source(enm)
        self.assertIsInstance(ret, str)
        util.finish(enm)

    def test_get_source_unget(self):
        enm = energymon()
        with self.assertRaises(ValueError):
            util.get_source(enm)

    def test_interval_us(self):
        enm = util.get_energymon(util.load_energymon_library())
        util.init(enm)
        ret = util.get_interval_us(enm)
        self.assertIsInstance(ret, int)
        self.assertTrue(ret >= 0)
        util.finish(enm)

    def test_interval_us_unget(self):
        enm = energymon()
        with self.assertRaises(ValueError):
            util.get_interval_us(enm)

    def test_precision_uj(self):
        enm = util.get_energymon(util.load_energymon_library())
        util.init(enm)
        ret = util.get_precision_uj(enm)
        self.assertIsInstance(ret, int)
        self.assertTrue(ret >= 0)
        util.finish(enm)

    def test_get_precision_uj_unget(self):
        enm = energymon()
        with self.assertRaises(ValueError):
            util.get_precision_uj(enm)

    def test_is_exclusive(self):
        enm = util.get_energymon(util.load_energymon_library())
        util.init(enm)
        ret = util.is_exclusive(enm)
        self.assertIsInstance(ret, bool)
        util.finish(enm)

    def test_is_exclusive_unget(self):
        enm = energymon()
        with self.assertRaises(ValueError):
            util.is_exclusive(enm)


if __name__ == '__main__':
    unittest.main()
