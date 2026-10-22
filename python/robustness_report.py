"""Robustness report: how far each sample drifts from a standard under the lights that matter.

Input: a CSV of spectral reflectances, first column wavelength in nm, then one column per
material; the first material column is the standard. Any range and interval inside 380-780 nm
works (it is interpolated to 380-780 nm at 5 nm; values outside the measured range are held at
the end values).

Output: a table of DeltaE(WLab) between each sample and the standard under each observing
condition, plus DeltaE00 under the first condition (normally the viewing booth), printed and
written to CSV.

    python robustness_report.py spectra.csv --conditions 1931:D50 1931:A 1931:F11 1964:D50 --out report.csv

Conditions are observer:illuminant with observer 1931, 1964 or 2015 and illuminant A, C, D50,
D65, E, F2 or F11. Tolerances are not built in: DeltaE(WLab) values are similar in size to
DeltaE00 values, and experience with your own products should set the limits.
"""

import argparse
import csv

import numpy as np

import wptonramp as w


def load_spectra(path, nm):
    with open(path, newline='') as f:
        rows = list(csv.reader(f))
    names = rows[0][1:]
    d = np.array([[float(v) for v in r] for r in rows[1:] if r])
    X = np.column_stack([np.interp(nm, d[:, 0], d[:, k]) for k in range(1, d.shape[1])])
    return names, X


def report(names, X, conditions, tables=None, base=None):
    """DeltaE(WLab) of every sample against the first column, per condition; DeltaE00 under the first."""
    T = tables or w.load_tables()
    base = base or w.load_base()
    out = []
    first = conditions[0]
    o0, i0 = T.observer[first[0]], T.illuminant[first[1]]
    lab = w.ref2lab(X, o0, i0)
    wl = {c: w.wpt_to_wlab(w.wpt_normalization(T.observer[c[0]], T.illuminant[c[1]], base).ref2wpt @ X) for c in conditions}
    for k in range(1, X.shape[1]):
        row = {'sample': names[k], f'DeltaE00 {first[0]}/{first[1]}': w.delta_e00(lab[:, :1], lab[:, k:k + 1])[0]}
        for c in conditions:
            row[f'DeltaE(WLab) {c[0]}/{c[1]}'] = w.delta_e_wlab(wl[c][:, :1], wl[c][:, k:k + 1])[0]
        out.append(row)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('spectra')
    ap.add_argument('--conditions', nargs='+', default=['1931:D50', '1931:D65', '1931:A', '1931:F11', '1964:D50'])
    ap.add_argument('--out')
    ap.add_argument('--light', action='append', default=[],
                    help='a measured light: CSV of nm,power, given as NAME=path; then use 1931:NAME in --conditions')
    a = ap.parse_args()
    T = w.load_tables()
    for spec in a.light:
        name, path = spec.split('=', 1)
        d = np.loadtxt(path, delimiter=',', skiprows=1)
        T.illuminant[name] = np.interp(T.nm, d[:, 0], d[:, 1], left=0, right=0)
    names, X = load_spectra(a.spectra, T.nm)
    conds = [tuple(c.split(':')) for c in a.conditions]
    rows = report(names, X, conds, T)
    keys = list(rows[0])
    print(f'Standard: {names[0]}')
    print('  '.join(f'{k:>22}' for k in keys))
    for r in rows:
        print('  '.join(f'{r[k]:>22.2f}' if isinstance(r[k], float) else f'{r[k]:>22}' for k in keys))
    if a.out:
        with open(a.out, 'w', newline='') as f:
            wr = csv.DictWriter(f, fieldnames=keys)
            wr.writeheader()
            wr.writerows({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()} for r in rows)


if __name__ == '__main__':
    main()
