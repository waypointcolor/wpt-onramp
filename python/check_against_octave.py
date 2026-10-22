"""Check the Python port against the Octave toolbox.

Compares the Wpt matrices for 14 observing conditions (excel/wpt_matrices.csv)
and the Wpt and WLab of 1,600 Munsell samples under CIE 1931 / D65
(results/check_1931_D65.csv), both written by octave/exportTables.m.
Run:  python check_against_octave.py
"""

import csv
from pathlib import Path

import numpy as np

import wptonramp as w

ROOT = Path(__file__).resolve().parent.parent
tables = w.load_tables()
base = w.load_base()

obs_key = {'CIE 1931 2deg': '1931', 'CIE 1964 10deg': '1964'}
worst = 0.0
with open(ROOT / 'excel' / 'wpt_matrices.csv', newline='') as f:
    for row in csv.DictReader(f):
        A = np.array([float(row[f'A{i}{j}']) for i in (1, 2, 3) for j in (1, 2, 3)]).reshape(3, 3)
        n = w.wpt_normalization(tables.observer[obs_key[row['observer']]], tables.illuminant[row['illuminant']], base)
        worst = max(worst, np.abs(n.xyz2wpt - A).max())
print(f'Wpt matrices, 14 conditions: largest difference from Octave {worst:.1e}')

mun = np.loadtxt(ROOT / 'toolbox' / 'munsell1600_380_780_5.csv', delimiter=',', skiprows=1)[:, 1:]
ref = np.loadtxt(ROOT / 'results' / 'check_1931_D65.csv', delimiter=',', skiprows=1).T
n = w.wpt_normalization(tables.observer['1931'], tables.illuminant['D65'], base)
wpt = n.ref2wpt @ mun
wlab = w.wpt_to_wlab(wpt)
print(f'1,600 Munsell samples, CIE 1931 / D65: largest Wpt difference {np.abs(wpt - ref[:3]).max():.1e}, '
      f'largest WLab difference {np.abs(wlab - ref[3:]).max():.1e}')
print(f'WLab back to Wpt: largest error {np.abs(w.wlab_to_wpt(wlab) - wpt).max():.1e}')
