"""
Context management for using an ``energymon``.
"""
from ctypes import CDLL
from typing import Union
import warnings
from . import util

class EnergyMon:
    """
    A wrapper class and context manager for an ``energymon``.

    As a context manager, it is both reentrant and reusable.

    Methods raise exceptions if the underlying native functions return an error.
    """

    def __init__(self, lib: Union[str, CDLL]='energymon-default',
                 func_get: str='energymon_get_default'):
        """
        Create a new instance.

        Parameters
        ----------
        lib : Union[str, ctypes.CDLL]
            The library name (a ``str``) or the library handler (a ``ctypes.CDLL``).
        func_get : str, optional
            The native "getter" function name to use.
        """
        # define _refcount first so if loading lib/energymon raises error, __del__ will still see it
        self._refcount = 0
        if isinstance(lib, str):
            lib = util.load_energymon_library(lib)
        self._ctx = util.get_energymon(lib, func_get)

    @property
    def initialized(self) -> bool:
        """bool: True if the ``energymon`` is initialized, False otherwise."""
        return self._refcount > 0

    def init(self):
        """
        Initialize the underlying ``energymon``.

        Only call this method if not using the pattern: ``with EnergyMon(...) as context:``.
        """
        if self._refcount > 0:
            raise ValueError('energymon is already initialized')
        util.init(self._ctx)
        self._refcount += 1

    def finish(self):
        """
        Finish the underlying ``energymon``.
        If not already initialized, this is a no-op.

        Only call this method if not using the pattern: ``with EnergyMon(...) as context:``.
        """
        if self._refcount > 0:
            self._refcount = 0
            util.finish(self._ctx)

    def _check_init(self):
        if not self.initialized:
            raise ValueError('energymon is not initialized')

    def get_uj(self) -> int:
        """
        Get the total energy in microjoules.

        Returns
        -------
        int
            The total energy in microjoules.
        """
        self._check_init()
        return util.get_uj(self._ctx)

    def get_source(self) -> str:
        """
        Get a human-readable description of the energy monitoring source.

        Initialization is not required to use this method.

        Returns
        -------
        str
            A human-readable description of the energy monitoring source.
        """
        return util.get_source(self._ctx)

    def get_interval_us(self) -> int:
        """
        Get the refresh interval in microseconds.

        Returns
        -------
        int
            The refresh interval in microseconds.
            This value should be greater than 0.
            If there is no minimum interval, returns 1.
        """
        self._check_init()
        return util.get_interval_us(self._ctx)

    def get_precision_uj(self) -> int:
        """
        Get the best possible possible read precision in microjoules.

        Returns
        -------
        int
            The best possible possible read precision in microjoules.
            If ``0 < precision <= 1``, returns 1.
            If the precision is unknown, returns 0.
        """
        self._check_init()
        return util.get_precision_uj(self._ctx)

    def is_exclusive(self) -> bool:
        """
        Get whether the implementation requires exclusive access.

        Initialization is not required to use this method.

        Returns
        -------
        bool
            True if the implementation requires exclusive access, False otherwise.
        """
        return util.is_exclusive(self._ctx)

    # Context management

    def __enter__(self):
        if self._refcount == 0:
            util.init(self._ctx)
        self._refcount += 1
        return self

    def __exit__(self, *args):
        # no-op if not initialized (user already called finish())
        if self._refcount > 0:
            self._refcount -= 1
            if self._refcount == 0:
                util.finish(self._ctx)

    # Safe cleanup

    def __del__(self):
        if self.initialized:
            warnings.warn('unfinished energymon', category=ResourceWarning, source=self)
            # force finish
            self._refcount = 0
            util.finish(self._ctx)

    # Limit copying and pickling

    def __getstate__(self):
        # deepcopy and pickling are never allowed b/c:
        # "ValueError: ctypes objects containing pointers cannot be pickled"
        # There's little value in supporting a shallow copy that doesn't keep the context - the user
        # would have to know to reinitialize, which also requires them to know lib and func_get...
        # The only safe way to support even a shallow copy is to keep refcount and ctx in shared
        # memory using multiprocess support, but this is a lot of overhead for a simple use case.
        # It would not be true multiprocess anyway, since the context uses function pointers which
        # are limited to the current process address space.
        raise TypeError(f"Cannot pickle {self.__class__.__name__!r} object")
