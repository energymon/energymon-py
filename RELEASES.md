# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Example program now uses `util.load_energymon_library`.


## [0.0.2] - 2021-11-23

### Added
- Function `util.load_energymon_library`.
- Minimum Python version specification in setup.
- Sphinx documentation - published on [Read the Docs](https://energymon-py.readthedocs.io/).
- Unit tests.

### Changed
- Minimum Python version is now 3.6.
- Use `c_uint64` instead of `c_ulonglong` for `energymon` `fread`, `finterval`, and `fprecision` return types.

### Removed
- The `energymon` submodule - C structure bindings now specified at module top level.


## [0.0.1] - 2021-08-10

- Initial release

[Unreleased]: https://github.com/energymon/energymon-py/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/energymon/energymon-py/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/energymon/energymon-py/releases/tag/v0.0.1
