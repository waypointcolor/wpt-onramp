"""The guide's examples in Python. Each function matches an Octave script in ../octave.

Run all:   python examples.py
Run one:   python examples.py ex04
"""

import sys
from pathlib import Path

import numpy as np

import wptonramp as w

ROOT = Path(__file__).resolve().parent.parent
T = w.load_tables()
BASE = w.load_base()
NAMES, BASE_X, _ = BASE


def sample(name):
    return BASE_X[:, NAMES.index(name)]


def munsell1600():
    return np.loadtxt(ROOT / 'toolbox' / 'munsell1600_380_780_5.csv', delimiter=',', skiprows=1)[:, 1:]


def norm(obs, ill):
    return w.wpt_normalization(T.observer[obs], T.illuminant[ill], BASE)


def ex01():
    """A material does not have one CIELAB value."""
    names = ['5R 5/6', '5G 5/6', '5PB 5/6', '50% gray']
    R = np.column_stack([sample(n) for n in names[:3]] + [0.5 * np.ones(len(T.nm))])
    o = T.observer['1931']
    print('CIELAB (L*, a*, b*), CIE 1931 observer; last column DeltaE00 from D65 to A')
    for k, n in enumerate(names):
        labs = {i: w.ref2lab(R[:, k], o, T.illuminant[i])[:, 0] for i in ('D65', 'A', 'F11')}
        cells = '   '.join(f'{i:>3} {l[0]:6.1f} {l[1]:6.1f} {l[2]:6.1f}' for i, l in labs.items())
        print(f'{n:<10} {cells}   {w.delta_e00(labs["D65"], labs["A"])[0]:5.1f}')


def ex02():
    """The worked example: Purplish Blue and its metameric twin (needs data/, see DATA.md)."""
    try:
        c = np.loadtxt(ROOT / 'data' / 'ColorChecker_380-780-5nm.txt')[:, 1:]
        m = np.loadtxt(ROOT / 'data' / 'MetaChecker_380-780-5nm.txt')[:, 1:]
    except OSError:
        print('ex02: put ColorChecker_380-780-5nm.txt and MetaChecker_380-780-5nm.txt in data/ (see DATA.md)')
        return
    o, k = T.observer['1931'], 7
    nD, nA = norm('1931', 'D65'), norm('1931', 'A')
    labD = lambda r: w.ref2lab(r, o, T.illuminant['D65'])
    labA = lambda r: w.ref2lab(r, o, T.illuminant['A'])
    wlD = lambda r: w.wpt_to_wlab(nD.ref2wpt @ r)
    wlA = lambda r: w.wpt_to_wlab(nA.ref2wpt @ r)
    fmt = lambda v: ' '.join(f'{x:6.1f}' for x in np.ravel(v))
    print('Purplish Blue, CIE 1931 observer      real patch            twin')
    for label, f in (('CIELAB under D65', labD), ('CIELAB under A', labA), ('WLab under D65', wlD), ('WLab under A', wlA)):
        print(f'{label:<26} {fmt(f(c[:, k]))}   {fmt(f(m[:, k]))}')
    print(f'CIELAB change, DeltaE00   {w.delta_e00(labD(c[:, k]), labA(c[:, k]))[0]:18.1f} {w.delta_e00(labD(m[:, k]), labA(m[:, k]))[0]:21.1f}')
    print(f'WLab change, DeltaE(WLab) {w.delta_e_wlab(wlD(c[:, k]), wlA(c[:, k]))[0]:18.1f} {w.delta_e_wlab(wlD(m[:, k]), wlA(m[:, k]))[0]:21.1f}')
    # the familiar alternative: carry the A values to D65 with a CAT (CAT02, full adaptation) before comparing
    cat02 = np.array([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
    wd, wa = (w.ref2xyz(np.ones(len(T.nm)), o, T.illuminant[i]) for i in ('D65', 'A'))
    mcat = np.linalg.solve(cat02, np.diag(((cat02 @ wd) / (cat02 @ wa))[:, 0]) @ cat02)
    labC = lambda r: w.xyz_to_lab(mcat @ w.ref2xyz(r, o, T.illuminant['A']), wd)
    print(f'CIELAB with CAT02, change  {w.delta_e00(labD(c[:, k]), labC(c[:, k]))[0]:18.1f} {w.delta_e00(labD(m[:, k]), labC(m[:, k]))[0]:21.1f}')
    C, M = c[:, :18], m[:, :18]
    lab_more = np.sum(w.delta_e00(labD(C), labA(C)) > w.delta_e00(labD(M), labA(M)))
    cat_more = np.sum(w.delta_e00(labD(C), labC(C)) > w.delta_e00(labD(M), labC(M)))
    wl_more = np.sum(w.delta_e_wlab(wlD(C), wlA(C)) > w.delta_e_wlab(wlD(M), wlA(M)))
    print(f'Of 18 chromatic patches, the real patch moves more than its twin: CIELAB {lab_more}, CIELAB with CAT02 {cat_more}, WLab {wl_more}')


def ex03():
    """The 40 base colors in Wpt under the reference condition (CIE 1931, illuminant C)."""
    n = norm('1931', 'C')
    wpt = n.ref2wpt @ np.column_stack([np.ones(len(T.nm)), BASE_X])
    ch = np.hypot(wpt[1, 1:], wpt[2, 1:])
    print(f'White: W {wpt[0, 0]:.2f}, p {wpt[1, 0]:.2f}, t {wpt[2, 0]:.2f}')
    print(f'40 colors: W {wpt[0, 1:].min():.2f} to {wpt[0, 1:].max():.2f}; chroma mean {ch.mean():.2f}, range {ch.min():.2f} to {ch.max():.2f}')


def ex04():
    """From a spectrum to Wpt and WLab, with sanity checks."""
    r = sample('5PB 5/6')
    print('1. Munsell 5PB 5/6, CIE 1931 observer')
    for i in ('D65', 'A', 'F11'):
        n = norm('1931', i)
        xyz = w.ref2xyz(r, T.observer['1931'], T.illuminant[i])
        wpt = n.xyz2wpt @ xyz
        f = lambda v: ' '.join(f'{x:6.2f}' for x in np.ravel(v))
        print(f'   {i:<4} XYZ {f(xyz)}  Wpt {f(wpt)}  WLab {f(w.wpt_to_wlab(wpt))}')
    print('2. 50% gray: ' + '; '.join(f'{i} WLab {np.round(w.wpt_to_wlab(norm("1931", i).ref2wpt @ (0.5 * np.ones(len(T.nm))))[:, 0], 2)}' for i in ('D65', 'A', 'F11')))
    X = munsell1600()
    wpt = norm('1931', 'D65').ref2wpt @ X
    print(f'3. WLab back to Wpt, {X.shape[1]} Munsell samples: largest error {np.abs(w.wlab_to_wpt(w.wpt_to_wlab(wpt)) - wpt).max():.1e}')
    M = np.array([[1.94735469, -1.41445123, 0.36476327], [0.68990272, 0.34832189, 0], [0, 0, 1.93485343]])
    lms = np.linalg.solve(M, T.observer['2015'].T).T
    a = w.wpt_normalization(T.observer['2015'], T.illuminant['D65'], BASE).ref2wpt @ X
    b = w.wpt_normalization(lms, T.illuminant['D65'], BASE).ref2wpt @ X
    print(f'4. CIE 2015 observer as XYZ functions or as LMS: largest Wpt difference {np.abs(a - b).max():.1e}')


def ex05():
    """CATs and MATs: illuminant A to D65, and converting an observer."""
    X, o = munsell1600(), T.observer['1931']
    src, dst = T.illuminant['A'], T.illuminant['D65']
    xs, xd = w.ref2xyz(X, o, src), w.ref2xyz(X, o, dst)
    ws, wd = w.ref2xyz(np.ones(len(src)), o, src), w.ref2xyz(np.ones(len(dst)), o, dst)
    true = w.xyz_to_lab(xd, wd)
    score = lambda xyz: w.delta_e00(w.xyz_to_lab(xyz, wd), true).mean()
    cat = lambda S: np.linalg.solve(S, np.diag(((S @ wd) / (S @ ws))[:, 0]) @ S)
    bradford = np.array([[0.8951, 0.2664, -0.1614], [-0.7502, 1.7135, 0.0367], [0.0389, -0.0685, 1.0296]])
    cat02 = np.array([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
    print(f'1. Illuminant A to D65, {X.shape[1]} Munsell samples, mean DeltaE00 from the true D65 values')
    for label, xyz in (('no adjustment', xs), ('white scaling in XYZ', cat(np.eye(3)) @ xs), ('Bradford CAT', cat(bradford) @ xs),
                       ('CAT02', cat(cat02) @ xs), ('Wpt MAT', w.mat(norm('1931', 'A'), norm('1931', 'D65')) @ xs)):
        print(f'   {label:<22} {score(xyz):5.2f}')
    o15 = T.observer['2015']
    M = w.mat(w.wpt_normalization(o15, dst, BASE), w.wpt_normalization(o, dst, BASE))
    lab31 = w.ref2lab(X, o, dst)
    print('2. CIE 2015 2-degree observer to CIE 1931 under D65, mean DeltaE00 from true 1931 values')
    print(f'   2015 functions used as they are   {w.delta_e00(w.ref2lab(X, o15, dst), lab31).mean():5.2f}')
    print(f'   2015 functions converted by MAT   {w.delta_e00(w.ref2lab(X, (M @ o15.T).T, dst), lab31).mean():5.2f}')


def ex06():
    """Color inconstancy and metamerism, measured in WLab, with a metameric twin made here."""
    r1 = sample('5PB 5/6')
    K = T.observer['1931'].T * T.illuminant['D65']
    Kp = np.linalg.pinv(K)
    r2 = r1 + 0.25 * np.sin(2 * np.pi * (T.nm - 380) / 90)
    for _ in range(200):
        r2 = np.clip(r2, 0, 1)
        r2 = r2 - Kp @ (K @ r2 - K @ r1)
    conds = [('1931', 'D65'), ('1931', 'A'), ('1931', 'F11'), ('1964', 'D65')]
    wl = {c: w.wpt_to_wlab(norm(*c).ref2wpt @ np.column_stack([r1, r2])) for c in conds}
    ref = wl[conds[0]]
    print('5PB 5/6 and its twin, DeltaE(WLab): between them / sample moved / twin moved (from 1931, D65)')
    for c in conds:
        d = w.delta_e_wlab(wl[c][:, :1], wl[c][:, 1:])[0]
        print(f'   CIE {c[0]}, {c[1]:<4} {d:6.2f} {w.delta_e_wlab(wl[c][:, :1], ref[:, :1])[0]:8.2f} {w.delta_e_wlab(wl[c][:, 1:], ref[:, 1:])[0]:8.2f}')


if __name__ == '__main__':
    pick = sys.argv[1:] or ['ex01', 'ex02', 'ex03', 'ex04', 'ex05', 'ex06']
    for name in pick:
        print(f'##### {name}')
        globals()[name]()
