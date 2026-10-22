"""wptonramp - Wpt, WLab and material adjustment transforms (MATs) in Python.

A port of the Octave toolbox in ../toolbox, for the examples that go with the
guide "Color Without the Fine Print". Arrays follow the Octave layout: spectra
are columns (wavelength x samples) and color coordinates are columns (3 x samples).

    tables = load_tables()                       # CIE observers and illuminants, 380-780 nm
    obs, ill = tables.observer['1931'], tables.illuminant['D65']
    w = wpt_normalization(obs, ill)              # Wpt normalization for that condition
    wpt = w.xyz2wpt @ ref2xyz(reflectance, obs, ill)
    wlab = wpt_to_wlab(wpt)

The tables are written by ../octave/exportTables.m, so both languages use the
same numbers.
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np

TOOLBOX = Path(__file__).resolve().parent.parent / 'toolbox'


@dataclass
class Tables:
    nm: np.ndarray            # wavelengths, 380:5:780
    observer: dict            # '1931', '1964', '2015': 81 x 3 color-matching functions
    illuminant: dict          # 'A', 'C', 'D50', 'D65', 'E', 'F2', 'F11': length-81 spectra


@dataclass
class WptNormalization:
    xyz2wpt: np.ndarray       # 3 x 3: the condition's sensor responses (white Y = 100) to Wpt
    ref2wpt: np.ndarray       # 3 x 81: reflectance straight to Wpt
    observer: np.ndarray
    illuminant: np.ndarray

    @property
    def wpt2xyz(self):
        return np.linalg.inv(self.xyz2wpt)


def load_tables():
    d = np.genfromtxt(TOOLBOX / 'spectral_tables_380_780_5.csv', delimiter=',', names=True)
    obs = {'1931': ('cie1931_x', 'cie1931_y', 'cie1931_z'),
           '1964': ('cie1964_x', 'cie1964_y', 'cie1964_z'),
           '2015': ('cie2015_2_x', 'cie2015_2_y', 'cie2015_2_z')}
    ill = {'A': 'illA', 'C': 'illC', 'D50': 'illD50', 'D65': 'illD65', 'E': 'illE', 'F2': 'illF2', 'F11': 'illF11'}
    return Tables(nm=d['nm'],
                  observer={k: np.column_stack([d[c] for c in v]) for k, v in obs.items()},
                  illuminant={k: d[v] for k, v in ill.items()})


def load_base():
    """The 40 Munsell reflectances (Value 5, Chroma 6) and their reference p, t."""
    f = TOOLBOX / 'wpt_base_munsell40.csv'
    names = f.read_text().splitlines()[0].split(',')[1:]
    X = np.loadtxt(f, delimiter=',', skiprows=1)[:, 1:]
    pt = np.loadtxt(TOOLBOX / 'wpt_reference_pt.csv', delimiter=',', skiprows=1, usecols=(1, 2))
    return names, X, pt.T


def ref2xyz(R, obs, ill):
    """Tristimulus values (or any sensor responses) of reflectances R, white Y = 100."""
    k = 100.0 / np.sum(obs[:, 1] * ill)
    return k * obs.T @ (ill[:, None] * np.asarray(R).reshape(len(ill), -1))


def wpt_normalization(obs, ill, base=None):
    """Wpt normalization for one observing condition (observer + illuminant).

    White goes onto the W axis at 100, the 40 base colors of one Munsell Value are
    leveled to one W, and a best fit puts them where they sit in the reference
    condition (CIE 1931, illuminant C). Same steps as getWptStruct.m.
    """
    _, X, mpt = base if base is not None else load_base()
    xyz = ref2xyz(X, obs, ill)
    lw = ref2xyz(np.ones(len(ill)), obs, ill)[:, 0]

    am = np.eye(3)                                  # 1. rotate white onto the first axis
    for d in (2, 1):
        phi = -np.arctan2(lw[d], lw[d - 1])
        r = np.eye(3)
        r[d - 1, d - 1], r[d - 1, d] = np.cos(phi), -np.sin(phi)
        r[d, d - 1], r[d, d] = np.sin(phi), np.cos(phi)
        lw, am = r @ lw, r @ am
    am[0] *= 100.0 / (am @ ref2xyz(np.ones(len(ill)), obs, ill))[0, 0]   # 2. white W = 100

    lxy = (am @ xyz).T                              # 3. level the equal-Value samples
    abc = np.linalg.pinv(np.column_stack([lxy[:, 1:], np.ones(len(lxy))])) @ lxy[:, 0]
    m2 = np.eye(3)
    m2[0, 1:] = -abc[:2]
    am = m2 @ am

    c = am @ xyz                                    # 4. best fit of p, t to the reference
    mc = mpt @ np.linalg.pinv(c[1:])
    fm = np.vstack([am[0], mc @ am[1:]])
    ref2wpt = fm @ obs.T * (ill * 100.0 / np.sum(obs[:, 1] * ill))
    return WptNormalization(xyz2wpt=fm, ref2wpt=ref2wpt, observer=obs, illuminant=ill)


def lab_to_lch(lab):
    lab = np.asarray(lab, float).reshape(3, -1)
    return np.vstack([lab[0], np.hypot(lab[1], lab[2]), np.degrees(np.arctan2(lab[2], lab[1])) % 360])


def lch_to_lab(lch):
    lch = np.asarray(lch, float).reshape(3, -1)
    h = np.radians(lch[2])
    return np.vstack([lch[0], lch[1] * np.cos(h), lch[1] * np.sin(h)])


_L5, _A, _GV = 51.576165618406904, 0.026742553710937, 0.458886718750000


def _hue_terms(h):
    r = np.zeros_like(h)
    s = (h > 1) & (h < 181)
    c = (h > 104) & (h < 284)
    r[s] = np.sin(np.radians(h[s] - 1)) ** 3
    r[c] += 0.39 * np.cos(np.radians(h[c] - 14)) ** 2
    return 62 * (r + 0.31), 0.36 * (r + 0.19)


def wpt_to_wlab(wpt):
    """Wpt to WLab (Lw, aw, bw). Same as Wpt2WLab.m."""
    w, c, h = lab_to_lch(wpt)
    y = w / 100
    lw = np.where(y > (6 / 29) ** 3, np.cbrt(y), (1 / 3) * (29 / 6) ** 2 * y + 16 / 116) * 116 - 16
    c = c / (np.exp(_A * (lw - _L5)) / _GV)
    b1, b2 = _hue_terms(h)
    c = b1 * (np.log(c / 80 + b2) - np.log(b2))
    return lch_to_lab(np.vstack([lw, c, h]))


def wlab_to_wpt(wlab):
    """WLab back to Wpt. Same as WLab2Wpt.m."""
    lw, c, h = lab_to_lch(wlab)
    b1, b2 = _hue_terms(h)
    c = 80 * (np.exp(c / b1 + np.log(b2)) - b2)
    c = c * (np.exp(_A * (lw - _L5)) / _GV)
    v = (lw + 16) / 116
    w = 100 * np.where(v > 6 / 29, v ** 3, (v - 4 / 29) * 3 * (6 / 29) ** 2)
    return lch_to_lab(np.vstack([w, c, h]))


def xyz_to_lab(xyz, white):
    """CIELAB, as XYZ2Lab.m."""
    f = np.asarray(xyz, float).reshape(3, -1) / np.asarray(white, float).reshape(3, 1)
    f = np.where(f > 0.008856, np.cbrt(f), 7.787 * f + 16 / 116)
    return np.vstack([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def ref2lab(R, obs, ill):
    return xyz_to_lab(ref2xyz(R, obs, ill), ref2xyz(np.ones(len(ill)), obs, ill))


def delta_e00(lab1, lab2):
    """CIEDE2000 (Sharma, Wu and Dalal 2005), as deltaE00.m."""
    L1, a1, b1 = np.asarray(lab1, float).reshape(3, -1)
    L2, a2, b2 = np.asarray(lab2, float).reshape(3, -1)
    cm = (np.hypot(a1, b1) + np.hypot(a2, b2)) / 2
    g = 0.5 * (1 - np.sqrt(cm ** 7 / (cm ** 7 + 25 ** 7)))
    ap1, ap2 = (1 + g) * a1, (1 + g) * a2
    cp1, cp2 = np.hypot(ap1, b1), np.hypot(ap2, b2)
    hp1 = np.where(cp1 == 0, 0, np.degrees(np.arctan2(b1, ap1)) % 360)
    hp2 = np.where(cp2 == 0, 0, np.degrees(np.arctan2(b2, ap2)) % 360)
    zero = cp1 * cp2 == 0
    dh = hp2 - hp1
    dh = np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh))
    dh = np.where(zero, 0, dh)
    dhp = 2 * np.sqrt(cp1 * cp2) * np.sin(np.radians(dh / 2))
    lpm, cpm, hs = (L1 + L2) / 2, (cp1 + cp2) / 2, hp1 + hp2
    far = np.abs(hp1 - hp2) > 180
    hpm = np.where(zero, hs, np.where(far & (hs < 360), (hs + 360) / 2, np.where(far, (hs - 360) / 2, hs / 2)))
    t = (1 - 0.17 * np.cos(np.radians(hpm - 30)) + 0.24 * np.cos(np.radians(2 * hpm))
         + 0.32 * np.cos(np.radians(3 * hpm + 6)) - 0.20 * np.cos(np.radians(4 * hpm - 63)))
    rc = 2 * np.sqrt(cpm ** 7 / (cpm ** 7 + 25 ** 7))
    sl = 1 + 0.015 * (lpm - 50) ** 2 / np.sqrt(20 + (lpm - 50) ** 2)
    sc, sh = 1 + 0.045 * cpm, 1 + 0.015 * cpm * t
    rt = -np.sin(np.radians(2 * 30 * np.exp(-((hpm - 275) / 25) ** 2))) * rc
    dl, dc, dhh = (L2 - L1) / sl, (cp2 - cp1) / sc, dhp / sh
    return np.sqrt(dl ** 2 + dc ** 2 + dhh ** 2 + rt * dc * dhh)


def delta_e_wlab(wlab1, wlab2):
    """The WLab difference: the straight-line distance between two WLab values."""
    return np.linalg.norm(np.asarray(wlab1, float).reshape(3, -1) - np.asarray(wlab2, float).reshape(3, -1), axis=0)


def mat(src, dst):
    """Material adjustment transform: source responses -> Wpt -> destination responses."""
    return np.linalg.solve(dst.xyz2wpt, src.xyz2wpt)
