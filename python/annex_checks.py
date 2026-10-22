"""Numbers quoted in the guide and its Technical annex that no example prints.

    python annex_checks.py          # writes ../results/annex_checks.log

1. Constant hue for a reflectance family a + b*Oc (annex A.3, guide "Properties worth knowing").
2. Chroma of the 40 base samples under the reference condition (annex A.4).
3. WLab with the 2015 paper's reference p, t against the toolbox reference (annex A.4).
4. WLab with the constants rounded as published (annex A.5).
5. Lw against CIELAB L* (guide "Sanity checks").
6. Two lights with the same white: D65 against a three-band LED with D65's X, Y, Z (guide "CATs and MATs").
"""

from pathlib import Path

import numpy as np

import wptonramp as w

ROOT = Path(__file__).resolve().parent.parent
T = w.load_tables()
NAMES, BASE_X, PT = w.load_base()
M1600 = np.loadtxt(ROOT / 'toolbox' / 'munsell1600_380_780_5.csv', delimiter=',', skiprows=1)[:, 1:]


def norm(obs, ill, base=(NAMES, BASE_X, PT)):
    return w.wpt_normalization(T.observer[obs], T.illuminant[ill], base)


def wlab(R, obs, ill, base=(NAMES, BASE_X, PT)):
    return w.wpt_to_wlab(norm(obs, ill, base).ref2wpt @ R)


def spread(h):
    h = np.unwrap(np.radians(h))
    return np.degrees(h.max() - h.min())


out = []
p = out.append

# 1. Munsell 5PB 5/6 with its minimum removed, a from 0 to 0.5, b from 0.3 to 1
oc = BASE_X[:, NAMES.index('5PB 5/6')]
oc = oc - oc.min()
a, b = np.meshgrid(np.linspace(0, 0.5, 11), np.linspace(0.3, 1, 15))
fam = a.ravel()[None, :] + b.ravel()[None, :] * oc[:, None]
p('1. Constant hue, Munsell 5PB 5/6 minus its minimum, a = 0..0.5, b = 0.3..1 (CIE 1931)')
for ill in ('D65', 'A'):
    lab_h = w.lab_to_lch(w.ref2lab(fam, T.observer['1931'], T.illuminant[ill]))[2]
    wpt_h = w.lab_to_lch(norm('1931', ill).ref2wpt @ fam)[2]
    p(f'   {ill:4s} CIELAB hue spread {spread(lab_h):5.2f} deg   Wpt hue spread {spread(wpt_h):.1e} deg')

# 2. Chroma of the base samples under the reference condition
c = w.lab_to_lch(norm('1931', 'C').ref2wpt @ BASE_X)[1]
p('2. Wpt chroma of the 40 base samples, CIE 1931 under C')
p(f'   min {c.min():.2f}  max {c.max():.2f}  mean {c.mean():.2f}  '
  f'standard deviation {c.std(ddof=1) / c.mean() * 100:.1f}% of the mean')

# 3. The 2015 paper's reference: p2015 = 1.01125 p, t2015 = t - 0.01331 p
pt15 = np.vstack([1.01125 * PT[0], PT[1] - 0.01331 * PT[0]])
p('3. WLab with the 2015 paper reference against the toolbox reference, 1600 Munsell, CIE 1931')
for ill in ('D50', 'D65'):
    d = w.delta_e_wlab(wlab(M1600, '1931', ill), wlab(M1600, '1931', ill, (NAMES, BASE_X, pt15)))
    p(f'   {ill:4s} largest {d.max():.2f}  mean {d.mean():.2f}')

# 4. Constants rounded as published
full = wlab(M1600, '1931', 'D65')
saved = w._L5, w._A, w._GV
w._L5, w._A, w._GV = 51.5762, 0.0267, 0.4589
d = w.delta_e_wlab(full, wlab(M1600, '1931', 'D65'))
w._L5, w._A, w._GV = saved
p('4. WLab with the published (rounded) constants, 1600 Munsell, CIE 1931 under D65')
p(f'   largest {d.max():.3f}  mean {d.mean():.3f}')

# 5. Lw against L*
p('5. Lw - L*, 1600 Munsell, CIE 1931')
for ill in ('C', 'D65', 'D50', 'A'):
    lw = wlab(M1600, '1931', ill)[0]
    ls = w.ref2lab(M1600, T.observer['1931'], T.illuminant[ill])[0]
    d = np.abs(lw - ls)
    p(f'   {ill:4s} largest {d.max():.2f}  mean {d.mean():.2f}')

# 6. A white LED of three narrow bands, weighted so that its white has exactly D65's X, Y, Z (CIE 1931).
# A CAT sees only the white, so it predicts no change; the Wpt MAT works from how materials respond.
obs, d65 = T.observer['1931'], T.illuminant['D65']
p('6. D65 against a three-band LED with the same white, 1600 Munsell, CIE 1931, DeltaE00')
for peaks, width in (((450, 540, 610), 12), ((455, 530, 620), 20)):
    bands = np.column_stack([np.exp(-0.5 * ((T.nm - c) / width) ** 2) for c in peaks])
    led = bands @ np.linalg.solve(obs.T @ bands, obs.T @ d65)
    lab_d65, lab_led = w.ref2lab(M1600, obs, d65), w.ref2lab(M1600, obs, led)
    change = w.delta_e00(lab_d65, lab_led)                       # also the CAT's error: it predicts no change
    mat = w.mat(w.wpt_normalization(obs, d65, (NAMES, BASE_X, PT)), w.wpt_normalization(obs, led, (NAMES, BASE_X, PT)))
    white_led = w.ref2xyz(np.ones(len(T.nm)), obs, led)[:, 0]
    err = w.delta_e00(w.xyz_to_lab(mat @ w.ref2xyz(M1600, obs, d65), white_led), lab_led)
    p(f'   bands at {peaks} nm, {width} nm wide: colors change by mean {change.mean():.2f}, largest {change.max():.1f} '
      f'(= CAT error); Wpt MAT error mean {err.mean():.2f}, largest {err.max():.1f}')

text = '\n'.join(out) + '\n'
print(text, end='')
(ROOT / 'results' / 'annex_checks.log').write_text(text)
