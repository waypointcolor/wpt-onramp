# wpt-onramp

Code and spreadsheets that go with the guide **WLab and Wpt: Color Without the Fine Print. An Onramp
to Material Color Equivalency**. Every number the guide computes can be reproduced here, in
GNU Octave (or MATLAB), in Python, or in a spreadsheet, and each example is a starting point for
your own experiments. (Results the guide quotes from the published papers, such as the
5,162-reflectance MAT test, are not rerun here; `ex05` runs a smaller version of that test.)

The equations themselves, with every constant and the reference coordinates of the 40 base
samples, are in the guide's **Technical annex**; its section A.8 maps each equation to the file
that implements it here.

- **The guide:** [WLab-Color-Without-the-Fine-Print.pdf](WLab-Color-Without-the-Fine-Print.pdf), with the Technical annex at the end (also readable here as [Markdown](WLab-Color-Without-the-Fine-Print.md))

## What is here

| Folder | What it holds |
| --- | --- |
| `octave/` | The examples as Octave scripts (`ex01` to `ex06`), and `exportTables.m`, which writes the tables the other languages read |
| `python/` | `wptonramp.py` (a port of the toolbox), `examples.py` (the same six examples), `robustness_report.py`, `hue_planes.py`, `annex_checks.py` (numbers the annex quotes that no example prints), and `check_against_octave.py` |
| `figures/` | The figures of the guide (the guide itself, as PDF and Markdown, is at the top of the repository) |
| `excel/` | `WLab-robustness-report.xlsx` (buyers: spectra in, report out, custom lights included); `WLab-calculator.xlsx` (XYZ to Wpt, WLab and CIELAB, the three color differences, a MAT sheet); `Wpt-normalization.xlsx` (the normalization and MATs step by step); `wpt_matrices.csv` behind them |
| `toolbox/` | The Wpt toolbox (Octave), CIE tables, the Munsell reflectances that carry the Wpt normalization, and CSV copies for Python |
| `data/` | Spectra you supply for `ex02` (see `data/README.md`); empty in the repository |
| `results/` | Logs of every run, so you can compare your output |

## The examples, by section of the guide

| Guide section | Example | What it shows |
| --- | --- | --- |
| What you may already know; A material does not have one Lab value | `ex01_cielab_moves` | CIELAB of the same samples under D65, A and F11: it moves, and by a different amount for each sample; a flat gray does not |
| A material does not have one Lab value; WLab (the example, revisited) | `ex02_purplish_blue` | The guide's worked example: a ColorChecker patch and its MetaChecker twin, in CIELAB, in CIELAB after a CAT (CAT02), and in WLab. Needs `data/`; `ex06` shows the same effect with included data only |
| Wpt: coordinates for the material | `ex03_reference_samples` | The 42 samples that set up Wpt, in Wpt: white at W = 100, the 40 colors on one level and near one circle, the yellow at t = 100 |
| Wpt; WLab; Getting started | `ex04_wpt_and_wlab` | The recipe from spectrum to WLab; sanity checks (50% gray is WLab 76.1, 0, 0 under every light; WLab converts back exactly; cone fundamentals and color-matching functions give the same Wpt) |
| CATs and MATs | `ex05_mats` | Illuminant A to D65 for 1,600 Munsell samples: Wpt MAT against Bradford, CAT02 and white scaling; converting the CIE 2015 observer to CIE 1931 |
| What you can do with it | `ex06_inconstancy_metamerism` | A metameric twin made from a Munsell sample; color inconstancy and metamerism under other lights and for another observer, in WLab |

## For buyers and managers

`excel/WLab-robustness-report.xlsx` is the buyer's tool: paste spectral reflectance (380-730 nm at
10 nm) of a standard and up to ten samples, pick up to six conditions from the list, and the Report
sheet shows DeltaE(WLab) between each sample and the standard under each condition, plus DeltaE00
under the first (normally the viewing booth). Your own lights go on the Custom lights sheet (paste a
measured spectrum, 380-780 nm at 5 nm); the workbook builds their Wpt normalization in-sheet and adds
them to the list. No macros.

`excel/Wpt-normalization.xlsx` is for technical users: pick or paste an observer and a light for a
source and a destination, and see each Wpt normalization in its four steps (Technical annex A.3),
the MAT between them, an XYZ converter and the source observer's functions converted by the MAT.
It replaces the original Wpt normalization spreadsheet, and uses the toolbox reference (see the
annex, A.4).

Both workbooks were recalculated in LibreOffice and checked against the Python code
(`results/workbooks_check.log`: within 6e-10).

`python/robustness_report.py` does the same from a CSV, for any range inside 380-780 nm.

```
..\.venv\Scripts\python robustness_report.py spectra.csv --conditions 1931:D50 1931:A 1931:F11 1964:D50 --out report.csv
```

The CSV has wavelength (nm) in the first column and one column per material, standard first;
any range and interval inside 380-780 nm works. No tolerances are built in: DeltaE(WLab) values are
designed to be similar in size to familiar DeltaE values, and experience with your own products should set the limits.
`python/make_buyer_example.py` makes the guide's example (a brand red and two submissions that both
match it exactly in a D50 booth) from the included Munsell set; its output is in `results/`.

## Gamut mapping: judging hue lines by eye

`python/hue_planes.py H1 H2 ...` draws, for each WLab hue angle, chips from gray to vivid (lightness
up, chroma across) split on the diagonal: the upper-left half holds WLab hue constant, the lower-right
half has the same L* and C*ab at the CIELAB hue of the ringed chip (the darkest of the most vivid;
`--anchor light` for the lightest). Where the halves differ, the two kinds of hue line disagree; judge
by eye which keeps the hue. The condition is CIE 1931 under D50, the ICC PCS, shown through a Bradford
adaptation to sRGB. `results/hue_planes_029_138_294.svg` is the picture in the guide. Gamut mapping
in WLab is an option to try and judge on your own work.

## Running them

**Octave or MATLAB.** From the `octave` folder: `ex04_wpt_and_wlab` (and so on). Each script finds
the toolbox itself. `ex02` stops with a message if the ColorChecker files are not in `data/`.

**Python 3** with numpy:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r python/requirements.txt
cd python
..\.venv\Scripts\python examples.py          # all six; or: examples.py ex05
..\.venv\Scripts\python check_against_octave.py
..\.venv\Scripts\python annex_checks.py      # numbers quoted in the Technical annex
```

**Spreadsheet.** Open `excel/WLab-calculator.xlsx` in Excel or LibreOffice. Yellow cells are
inputs. The workbook has no macros. It was recalculated in LibreOffice and checked against the
Python code (`results/spreadsheet_check.log`).

## How the three agree

`octave/exportTables.m` writes the CIE tables, the Munsell base set, its reference p and t, and
the Wpt matrices for 14 conditions. Python and the spreadsheet use only those files.

| Check | Largest difference | Log |
| --- | --- | --- |
| Python Wpt matrices against Octave, 14 conditions | 2e-10 | `results/python_check.log` |
| Python Wpt and WLab of 1,600 Munsell samples against Octave | 7e-8 | `results/python_check.log` |
| Python examples against Octave examples | identical to the printed digits | `results/python_examples.log`, `results/ex*.log` |
| Spreadsheet against Python (LibreOffice recalculation) | 1e-10 | `results/spreadsheet_check.log` |

## Notes

- Wpt and WLab work for any observer: the CIE standard observers, the CIE 2006 and 2015
  observers, a camera. The Octave and Python code build the normalization for whatever curves
  you give them; the spreadsheet lists 14 common conditions and takes more rows on its Matrices sheet.
- WLab differences are material color differences. They correspond to perceived color differences
  under a reference observing condition, as CIELAB-based formulas such as DeltaE00 do; WLab is not
  a color appearance space.
- Wpt reduces color inconstancy; it does not remove it.

## References

- Derhak MW, Berns RS. Introducing Wpt (Waypoint): a color equivalency representation for defining
  a material adjustment transform. Color Res Appl 2015;40(6):535-549. https://doi.org/10.1002/col.21928
- Derhak MW, Berns RS. Introducing WLab: going from Wpt (Waypoint) to a uniform material color
  equivalency space. Color Res Appl 2015;40(6):550-563. https://doi.org/10.1002/col.21933

## License

- The guide and its Technical annex: Creative Commons Attribution 4.0 (CC BY 4.0); see [LICENSE-guide.md](LICENSE-guide.md).
- The workbooks (their formulas and layout) and the code in `octave/`, `python/` and `toolbox/`: BSD 3-Clause; see [LICENSE](LICENSE).
- The CIE data, in `toolbox/`, `excel/wpt_matrices.csv` and on the workbooks' data sheets: licensed by the CIE under CC BY-SA 4.0, with the Wpt matrices calculated from them under the same license. [DATA.md](DATA.md) lists each CIE dataset with its DOI and the sources of the other data.
- The Munsell reflectances: measured by the University of Eastern Finland (formerly Joensuu) and corrected by Derhak and Berns (2012); see [DATA.md](DATA.md). Please credit both when using them.

Maxim W. Derhak, Onyx Graphics Inc.
