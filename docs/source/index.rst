.. energymon documentation master file, created by
   sphinx-quickstart on Mon Nov 15 15:19:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EnergyMon Python Bindings
=========================

This project provides Python bindings to `energymon <https://github.com/energymon/energymon>`_ libraries.

Installation
------------

The package is available on `PyPI <https://pypi.org/project/energymon/>`_:

.. code::

    pip install energymon

and on `Conda Forge <https://anaconda.org/conda-forge/energymon>`_:

.. code::

    conda install energymon


Getting Started
---------------

The energymon libraries should be installed to the system and on the library search path (e.g., ``LD_LIBRARY_PATH`` on Linux/POSIX systems or ``DYLD_LIBRARY_PATH`` on macOS systems).

The simplest and most Pythonic approach is to use the ``EnergyMon`` context manager.
For example, to measure the energy consumption of a task using the ``energymon-default`` library:

.. code-block::

   from energymon.context import EnergyMon

   with EnergyMon() as em:
       print('Energy source:', em.get_source())
       uj_start = em.get_uj()
       # do some non-trivial work (must take longer than the energy source's update interval)
       uj_end = em.get_uj()
   print('Energy (uJ):', uj_end - uj_start)


Specify the ``lib`` and ``func_get`` parameters when instantiating ``EnergyMon`` to use other energymon libraries.

Direct C struct bindings are also available using the ``energymon`` ctypes class.
See the README in the `project source <https://github.com/energymon/energymon-py>`_ for a detailed example.


API Reference
=============

.. toctree::
   :maxdepth: 2

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
