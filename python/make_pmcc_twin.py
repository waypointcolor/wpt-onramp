"""Make the landing page's metameric pairs: patches of a Preferred Memory Colour Chart (PMCC), as measured by Maxim W.
Derhak, each with a twin that matches it exactly for the CIE 1931 observer under D65.

    .venv/Scripts/python python/make_pmcc_twin.py PMCC-Refs-380_10_730.txt [patch ...]

The patches are Smurf and Unitary Blue unless named.
The measurement file has one patch per row: "PMCC <name>" and 36 reflectance factors, 380 to 730 nm at 10 nm. The
patch is interpolated to 5 nm and its 730 nm value held to 780 nm. The twin is made as in ex06: the patch plus a
wave, clipped to 0..1 and projected back onto the patch's CIE 1931/D65 tristimulus values, repeated until both hold.
Writes results/pmcc_<patch>_twin.csv and .log for each patch (for example pmcc_unitary_blue_twin.csv).
"""
import sys
from pathlib import Path

import numpy as np

import wptonramp as w

ROOT = Path(__file__).resolve().parent.parent
T = w.load_tables()
BASE = w.load_base()


def main(src, PATCH):
    slug = PATCH.lower().replace(' ', '_')
    rows = [ln.rstrip('\n').split('\t') for ln in open(src, encoding='utf-8') if ln.strip()]
    row = next(r for r in rows if r[0] == 'PMCC ' + PATCH)
    r1 = np.interp(T.nm, np.arange(380, 731, 10), [float(x) for x in row[1:]])
    K = T.observer['1931'].T * T.illuminant['D65']
    Kp = np.linalg.pinv(K)
    r2 = r1 + 0.25 * np.sin(2 * np.pi * (T.nm - 380) / 90)
    for _ in range(200):
        r2 = np.clip(r2, 0, 1)
        r2 = r2 - Kp @ (K @ r2 - K @ r1)
    r2 = np.round(r2, 6)
    np.savetxt(ROOT / 'results' / f'pmcc_{slug}_twin.csv', np.column_stack([T.nm, r1, r2]), delimiter=',',
               header=f'nm,pmcc_{slug},twin', comments='', fmt=['%d', '%.6f', '%.6f'])

    def lab(r, obs, ill):
        return w.ref2lab(r, T.observer[obs], T.illuminant[ill])

    def wlab(r, obs, ill):
        return w.wpt_to_wlab(w.wpt_normalization(T.observer[obs], T.illuminant[ill], BASE).ref2wpt @ r[:, None])

    out = [f'PMCC {PATCH} and its twin; twin reflectance {r2.min():.3f} to {r2.max():.3f}',
           'Change from CIE 1931, D65 (DeltaE00 / DeltaE WLab), and between the two (DeltaE WLab)']
    for c in [('1931', 'D65'), ('1931', 'D50'), ('1931', 'A'), ('1931', 'F11'), ('1964', 'D65')]:
        moved = [(w.delta_e00(lab(r, '1931', 'D65'), lab(r, *c))[0],
                  w.delta_e_wlab(wlab(r, '1931', 'D65'), wlab(r, *c))[0]) for r in (r1, r2)]
        between = w.delta_e_wlab(wlab(r1, *c), wlab(r2, *c))[0]
        out.append(f'   CIE {c[0]}, {c[1]:<4}  {PATCH} {moved[0][0]:5.2f} / {moved[0][1]:5.2f}   '
                   f'twin {moved[1][0]:5.2f} / {moved[1][1]:5.2f}   between {between:5.2f}')
    text = '\n'.join(out) + '\n'
    (ROOT / 'results' / f'pmcc_{slug}_twin.log').write_text(text, encoding='utf-8')
    print(text, end='')


if __name__ == '__main__':
    for patch in sys.argv[2:] or ['Smurf', 'Unitary Blue']:
        main(sys.argv[1], patch)
