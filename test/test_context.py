# pylint: disable=C0114, C0116
import pickle
import unittest
from energymon import util
from energymon.context import EnergyMon

class TestEnergyMon(unittest.TestCase):
    """Test EnergyMon."""

    def test_create(self):
        enm = EnergyMon()
        self.assertFalse(enm.initialized)

    def test_create_with_cdll(self):
        enm = EnergyMon(lib=util.load_energymon_library())
        self.assertFalse(enm.initialized)

    def test_create_bad(self):
        with self.assertRaises(FileNotFoundError):
            EnergyMon(lib='!@#$%^&*()')
        with self.assertRaises(AttributeError):
            EnergyMon(func_get='!@#$%^&*()')

    def test_init_finish(self):
        enm = EnergyMon()
        self.assertIsNone(enm.init())
        self.assertTrue(enm.initialized)
        self.assertIsNone(enm.finish())
        self.assertFalse(enm.initialized)

    def test_double_init(self):
        enm = EnergyMon()
        enm.init()
        with self.assertRaises(ValueError):
            enm.init()
        self.assertTrue(enm.initialized)
        enm.finish()

    def test_double_finish(self):
        enm = EnergyMon()
        enm.init()
        enm.finish()
        self.assertIsNone(enm.finish())
        self.assertFalse(enm.initialized)

    def test_methods(self):
        enm = EnergyMon()
        enm.init()
        self.assertIsInstance(enm.get_uj(), int)
        self.assertIsInstance(enm.get_source(), str)
        self.assertIsInstance(enm.get_interval_us(), int)
        self.assertIsInstance(enm.get_precision_uj(), int)
        self.assertIsInstance(enm.is_exclusive(), bool)
        enm.finish()

    def test_methods_uninit(self):
        enm = EnergyMon()
        with self.assertRaises(ValueError):
            self.assertIsInstance(enm.get_uj(), int)
        self.assertIsInstance(enm.get_source(), str)
        with self.assertRaises(ValueError):
            self.assertIsInstance(enm.get_interval_us(), int)
        with self.assertRaises(ValueError):
            self.assertIsInstance(enm.get_precision_uj(), int)
        self.assertIsInstance(enm.is_exclusive(), bool)

    def test_del_warning(self):
        enm = EnergyMon()
        enm.init()
        with self.assertWarns(ResourceWarning):
            del enm

    def test_context(self):
        with EnergyMon() as enm:
            self.assertIsInstance(enm, EnergyMon)
            self.assertTrue(enm.initialized)

    def test_context_predefined(self):
        enm = EnergyMon()
        with enm:
            self.assertTrue(enm.initialized)
        self.assertFalse(enm.initialized)

    def test_context_reentrant(self):
        enm = EnergyMon()
        with enm:
            self.assertTrue(enm.initialized)
            with enm:
                self.assertTrue(enm.initialized)
            self.assertTrue(enm.initialized)
        self.assertFalse(enm.initialized)

    def test_context_reusable(self):
        enm = EnergyMon()
        with enm:
            self.assertTrue(enm.initialized)
        self.assertFalse(enm.initialized)
        with enm:
            self.assertTrue(enm.initialized)
        self.assertFalse(enm.initialized)

    def test_context_force_finish(self):
        enm = EnergyMon()
        with enm:
            self.assertTrue(enm.initialized)
            enm.finish()
            self.assertFalse(enm.initialized)
        self.assertFalse(enm.initialized)

    def test_context_with_manual_lifecycle(self):
        enm = EnergyMon()
        enm.init()
        self.assertTrue(enm.initialized)
        with enm:
            self.assertTrue(enm.initialized)
        self.assertTrue(enm.initialized)
        enm.finish()
        self.assertFalse(enm.initialized)

    def test_pickle(self):
        enm = EnergyMon()
        with self.assertRaises(TypeError):
            pickle.dumps(enm)


if __name__ == '__main__':
    unittest.main()
