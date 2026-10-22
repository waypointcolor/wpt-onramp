# Your own data

The guide's worked example (`ex02`) needs two files here, which are not part of the package:

- `ColorChecker_380-780-5nm.txt`: spectral reflectance of the 24 X-Rite ColorChecker patches, 380 to
  780 nm every 5 nm. Plain text, one row per wavelength: the wavelength, then one column per patch in
  the usual order (Dark Skin first, Black last).
- `MetaChecker_380-780-5nm.txt`: the MetaChecker, computed metamers of those patches for the CIE 1931
  observer under D65, in the same layout.

Everything else runs without them. See `../DATA.md`.
