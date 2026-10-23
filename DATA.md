# Data in this package

All spectral data run from 380 to 780 nm in 5 nm steps unless noted.

| File | Contents | Source |
| --- | --- | --- |
| `toolbox/CIE_2Deg_380-780-5nm.txt`, `toolbox/CIE_10Deg_380-780-5nm.txt` | CIE 1931 2° and CIE 1964 10° color-matching functions | CIE tables (CIE 15, Colorimetry), as used by the original Wpt code |
| `toolbox/CIE_2Deg-2015_380-830-1nm.txt`, `toolbox/CIE_10Deg-2015_380-830-1nm.txt` | CIE 2015 2° and 10° cone-fundamental-based color-matching functions, 1 nm | CIE 170-2:2015 |
| `toolbox/CIE_IllA_300-830-5nm.txt`, `toolbox/CIE_IllC_300-830-5nm.txt`, `toolbox/CIE_IllD65_300-830-5nm.txt`, `toolbox/CIE_IllF_1-12_380-780-5nm.txt` | Illuminants A, C, D65 and F1 to F12 | CIE tables (CIE 15) |
| `toolbox/CIE_eigD_380-780-5nm.txt` | Components of the CIE daylight illuminants; D50 is computed from them at 5000 K (`cieIllD.m`), as in the original Wpt code | CIE tables (CIE 15) |
| `toolbox/spectral_tables_380_780_5.csv` | The observers and illuminants above on one 5 nm grid, for Python and the workbooks | Written from the files above by `octave/exportTables.m` |
| `excel/wpt_matrices.csv` | Wpt matrices (XYZ to Wpt and back) for the CIE 1931 2° and CIE 1964 10° observers under illuminants C, D50, D65, A, E, F2 and F11, with the X, Y, Z of white | Computed from the CIE data and the Munsell base set by `octave/exportTables.m` |
| `toolbox/munsell380_780_5_reconstC.mat`, `toolbox/munsell1600_380_780_5.csv` | Reflectance factors of the 1,600 Munsell glossy colors, corrected to the Munsell renotation under illuminant C | See "The Munsell reflectances" below |
| `toolbox/wpt_base_munsell40.csv` | The 40 Munsell colors of Value 5 and Chroma 6 that carry the Wpt normalization (from the same set) | See below |
| `toolbox/wpt_reference_pt.csv` | Their reference p and t (CIE 1931 2° observer, illuminant C) | The Wpt toolbox (`getWptStruct.m`); the guide's Technical annex (A.4) says how they relate to the 2015 Wpt paper |
| `results/example_white_LED_made_up.csv` | A made-up white LED (a blue peak and two broad phosphor bands, Gaussian), the example custom light | Made for this package; its own data |
| `index.html` | The same tables, built into the landing page, and its demo data: the two PMCC pairs below, the buyer example and the made-up LED | Built from the same tables by the `wlab` TypeScript package |
| `WLab-robustness-report.html` | The CIE observers and illuminants and the Munsell base set above, built into the page, and the buyer example spectra | Built from the same tables by the `wlab` TypeScript package |
| `results/pmcc_smurf_twin.csv`, `results/pmcc_unitary_blue_twin.csv` | Two blues, each with its twin: the Smurf and Unitary Blue patches of a Preferred Memory Colour Chart (PMCC; M. R. Luo, "The new preferred memory color (PMC) chart," *Color Research & Application* 49(6), 564-576 (2024), DOI [10.1002/col.22940](https://doi.org/10.1002/col.22940)), measured by Maxim W. Derhak from 380 to 730 nm at 10 nm (interpolated here to 5 nm, the 730 nm value held to 780 nm), and for each a twin that matches it exactly for the CIE 1931 observer under D65 | The measurement: Maxim W. Derhak; the twins made by `python/make_pmcc_twin.py`; this package's own data |
| `results/buyer_example_spectra.csv` | A brand red (Munsell 5R 5/6) and two made-up submissions that match it exactly in a D50 booth, 380 to 730 nm at 10 nm | Made by `python/make_buyer_example.py` from the Munsell base set; this package's own data |

## Licenses

The CIE publishes its colorimetric data tables as open datasets under the [Creative Commons
Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
The files above that hold CIE data, or are calculated from it (`spectral_tables_380_780_5.csv`,
`wpt_matrices.csv`, `index.html`, `WLab-robustness-report.html`, and the CIE data on the workbooks' Tables, Weights and Matrices sheets), are
therefore licensed under CC BY-SA 4.0. The CIE datasets, as the CIE asks them to be cited:

- CIE 2019, Colour-matching functions of CIE 1931 standard colorimetric observer, CIE, Vienna, AT, DOI [10.25039/CIE.DS.xvudnb9b](https://doi.org/10.25039/CIE.DS.xvudnb9b)
- CIE 2019, CIE 1964 colour-matching functions, 10 degree observer, CIE, Vienna, AT, DOI [10.25039/CIE.DS.sqksu2n5](https://doi.org/10.25039/CIE.DS.sqksu2n5)
- CIE 2015, CIE cone-fundamental-based spectral tristimulus values for 2° field size, CIE, Vienna, AT, DOI [10.25039/CIE.DS.548rw69q](https://doi.org/10.25039/CIE.DS.548rw69q)
- CIE 2015, CIE cone-fundamental-based spectral tristimulus values for 10° field size, CIE, Vienna, AT, DOI [10.25039/CIE.DS.dm6qiig7](https://doi.org/10.25039/CIE.DS.dm6qiig7)
- CIE 2018, CIE standard illuminant A - 1 nm, CIE, Vienna, AT, DOI [10.25039/CIE.DS.8jsxjrsn](https://doi.org/10.25039/CIE.DS.8jsxjrsn)
- CIE 2018, Relative spectral power distributions of CIE illuminant C, CIE, Vienna, AT, DOI [10.25039/CIE.DS.mjdd2enu](https://doi.org/10.25039/CIE.DS.mjdd2enu)
- CIE 2019, CIE standard illuminant D65, CIE, Vienna, AT, DOI [10.25039/CIE.DS.hjfjmt59](https://doi.org/10.25039/CIE.DS.hjfjmt59)
- CIE 2018, Components of the relative spectral distribution of daylight used in the calculation of relative spectral power distributions of CIE daylight illuminants of different correlated colour temperatures, CIE, Vienna, AT, DOI [10.25039/CIE.DS.w7zunnny](https://doi.org/10.25039/CIE.DS.w7zunnny)
- CIE 2018, Relative spectral power distributions of illuminants representing typical fluorescent lamps, CIE, Vienna, AT, DOI [10.25039/CIE.DS.ukaymjdn](https://doi.org/10.25039/CIE.DS.ukaymjdn)

The values here were not downloaded from these datasets: they come from the tables used by the
original Wpt code (CIE 15 and CIE 170-2:2015). The datasets are cited because they are the CIE's
published, licensed form of the same tables. Illuminant E (equal energy) is constant and needs no
source. The made-up LED and the buyer example spectra are this package's own and are licensed under
the BSD 3-Clause License with the code.

## The Munsell reflectances

- **Measurements.** The Color Research Laboratory of the University of Joensuu (now the University of
  Eastern Finland, UEF) measured the 1,600 glossy chips of a Munsell Book of Color manufactured in 1976,
  with a Perkin-Elmer Lambda 18 spectrophotometer, from 380 to 780 nm at 1 nm. UEF publishes these
  measurements as "Munsell colors glossy (all) (Spectrofotometer measured)",
  https://sites.uef.fi/spectral/?p=423, © University of Eastern Finland.
- **Correction.** M. W. Derhak and R. S. Berns corrected each spectrum so that its colorimetry matches
  the Munsell renotation data: "Analysis and correction of the Joensuu Munsell glossy spectral
  database," Proc. 20th Color and Imaging Conference (IS&T, 2012), pp. 191-194. M. W. Derhak first
  published the corrected reflectances through the Munsell Color Science Laboratory at RIT; that page
  is no longer online.
- **Here.** The corrected set at 5 nm from 380 to 780 nm, published here by M. W. Derhak with the rest
  of the package. When using them, please credit both the UEF measurements and the 2012 correction paper.

## Not included: the ColorChecker and MetaChecker spectra

The guide's worked example (`octave/ex02_purplish_blue.m` and `python/examples.py ex02`) uses the
spectra of the X-Rite ColorChecker and of the MetaChecker, a set of computed metamers of its patches.
They are not distributed here. To run `ex02`, place them in `data/` as described in `data/README.md`.
`ex06` shows the same effect with a metameric twin built from the included Munsell data.
