"""Make the buyer example used in the guide: a brand red and two submissions that both match it
exactly in a D50 viewing booth (CIE 1931 observer).

The standard is Munsell 5R 5/6 from the included base set. Each submission adds a component the
CIE 1931 observer cannot see under D50: a gentle one for submission 1 (a smooth spectrum, like a
close formulation with similar colorants) and a strongly wavy one for submission 2 (a jagged
spectrum, like a match made with very different colorants). Writes
results/buyer_example_spectra.csv and results/buyer_example_report.csv.
"""

from pathlib import Path

import numpy as np

import robustness_report as rr
import wptonramp as w

ROOT = Path(__file__).resolve().parent.parent
T = w.load_tables()
names, X, _ = w.load_base()
# the spectra are made on the 10 nm grid that instruments report (380-730 nm), and used the way
# the tools use measured data: interpolated to 5 nm and held constant beyond 730 nm
GRID = np.arange(380, 731, 10)
P = np.column_stack([np.interp(T.nm, GRID, np.eye(len(GRID))[k]) for k in range(len(GRID))])
std = np.interp(GRID, T.nm, X[:, names.index('5R 5/6')])
K = T.observer['1931'].T @ (T.illuminant['D50'][:, None] * P)
Kp = np.linalg.pinv(K)


def twin(r, amplitude, period):
    t = r + amplitude * np.sin(2 * np.pi * (GRID - 380) / period)
    for _ in range(300):
        t = np.clip(t, 0, 1)
        t = t - Kp @ (K @ t - K @ r)
    return t


S10 = np.column_stack([std, twin(std, 0.04, 400), twin(std, 0.12, 70)])
S = P @ S10
labels = ['Brand red standard (5R 5/6)', 'Submission 1 (smooth)', 'Submission 2 (jagged)']
with open(ROOT / 'results' / 'buyer_example_spectra.csv', 'w') as f:
    f.write('nm,' + ','.join(labels) + '\n')
    for i, nm in enumerate(GRID):
        f.write(f'{nm:g},' + ','.join(f'{v:.5f}' for v in S10[i]) + '\n')

conds = [('1931', 'D50'), ('1931', 'D65'), ('1931', 'A'), ('1931', 'F2'), ('1931', 'F11'), ('1964', 'D50')]
rows = rr.report(labels, S, conds, T)
print(f'Both submissions within 0..1: {bool(np.all((S10 >= 0) & (S10 <= 1)))}; '
      f'largest XYZ difference under 1931/D50: {np.abs(K @ (S10[:, 1:] - S10[:, :1])).max():.1e}')
for r in rows:
    print(r['sample'], '  '.join(f'{k.split()[-1]} {v:.2f}' for k, v in r.items() if k != 'sample'))
with open(ROOT / 'results' / 'buyer_example_report.csv', 'w') as f:
    f.write(','.join(rows[0]) + '\n')
    for r in rows:
        f.write(','.join(f'{v:.3f}' if isinstance(v, float) else v for v in r.values()) + '\n')
