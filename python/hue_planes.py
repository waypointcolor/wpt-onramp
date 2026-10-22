"""Constant WLab hue against constant CIELAB hue, drawn as split sRGB chips, to judge hue lines for gamut mapping.

For each WLab hue angle H, chips are laid out with lightness up and chroma across, keeping only the
chips inside the sRGB gamut. Each chip is split on its diagonal:

- upper-left triangle: the WLab chip, at hue H;
- lower-right triangle: the CIELAB colour with the same L* and C*ab, but at the CIELAB hue of the
  anchor chip (ringed): the darkest of the most chromatic WLab chips (--anchor light: the lightest).

Where the two halves match, constant WLab hue and constant CIELAB hue agree; where they differ, a
gamut mapping that holds CIELAB hue would change the hue that WLab holds. The condition is the CIE
1931 observer under D50 (the ICC PCS), shown on screen through a Bradford adaptation to sRGB.

    python hue_planes.py 29 294 138 --out ../results/hue_planes_029_294_138.svg

Writes an SVG; open it in a browser, or convert it to PNG. Screen colours are approximate.
"""

import argparse

import numpy as np

import wptonramp as w

T = w.load_tables()
OBS, ILL = T.observer['1931'], T.illuminant['D50']
N = w.wpt_normalization(OBS, ILL, w.load_base())
WHITE = w.ref2xyz(np.ones(len(T.nm)), OBS, ILL)[:, 0]

RGB2XYZ = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
BFD = np.array([[0.8951, 0.2664, -0.1614], [-0.7502, 1.7135, 0.0367], [0.0389, -0.0685, 1.0296]])
W65 = RGB2XYZ @ np.ones(3) * 100
TO_RGB = np.linalg.inv(RGB2XYZ) @ np.linalg.inv(BFD) @ np.diag((BFD @ W65) / (BFD @ WHITE)) @ BFD


def lab_to_xyz(lab):
    L, a, b = np.asarray(lab, float).reshape(3, -1)
    fy = (L + 16) / 116
    f = np.vstack([fy + a / 500, fy, fy - b / 200])
    return np.where(f > 6 / 29, f ** 3, 3 * (6 / 29) ** 2 * (f - 4 / 29)) * WHITE.reshape(3, 1)


def srgb(xyz):
    lin = TO_RGB @ xyz / 100
    ok = np.all((lin >= -1e-9) & (lin <= 1 + 1e-9), axis=0)
    g = np.clip(lin, 0, 1)
    return np.where(g <= 0.0031308, 12.92 * g, 1.055 * g ** (1 / 2.4) - 0.055), ok


def hue(v):
    v = np.asarray(v, float).reshape(3, -1)
    return np.degrees(np.arctan2(v[2], v[1])) % 360


def plane(H, anchor='dark', stepL=5, stepC=5):
    Lv, Cv = np.arange(5, 96, stepL), np.arange(0, 91, stepC)
    Lg, Cg = (x.ravel() for x in np.meshgrid(Lv, Cv, indexing='ij'))
    xyz_w = N.wpt2xyz @ w.wlab_to_wpt(np.vstack([Lg, Cg * np.cos(np.radians(H)), Cg * np.sin(np.radians(H))]))
    rgb_w, ok_w = srgb(xyz_w)
    i = np.flatnonzero(ok_w)
    i = i[Cg[i] == Cg[i].max()]
    ia = i[np.argmin(Lg[i])] if anchor == 'dark' else i[np.argmax(Lg[i])]
    lab_w = w.xyz_to_lab(xyz_w, WHITE)
    hab = hue(lab_w[:, ia])[0]
    cab = np.hypot(lab_w[1], lab_w[2])
    rgb_l, ok_l = srgb(lab_to_xyz(np.vstack([lab_w[0], cab * np.cos(np.radians(hab)), cab * np.sin(np.radians(hab))])))
    gap = (hue(lab_w) - hab + 180) % 360 - 180
    bg, _ = srgb(N.wpt2xyz @ w.wlab_to_wpt(np.vstack([Lv, 0 * Lv, 0 * Lv]).astype(float)))
    return dict(H=H, hab=hab, Lv=Lv, Lg=Lg, Cg=Cg, rgb_w=rgb_w, ok_w=ok_w, rgb_l=rgb_l, ok_l=ok_l,
                gap=gap, bg=bg, anchor=ia, stepL=stepL, stepC=stepC)


def hexc(c):
    return '#%02x%02x%02x' % tuple(int(round(255 * v)) for v in c)


def svg(planes, anchor='dark'):
    chip, gap, rowgap, sep = 24, 2, 4, 36
    nL = len(planes[0]['Lv'])
    used = [int(P['Cg'][P['ok_w']].max() / P['stepC']) + 1 for P in planes]
    pws = [u * (chip + gap) + gap for u in used]
    ph = nL * (chip + rowgap) + rowgap
    x0, y0 = 64, 148
    W = max(760, x0 + sum(pws) + sep * (len(planes) - 1) + 24)
    H = y0 + ph + 104
    o = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}' font-family='Segoe UI, Helvetica, Arial, sans-serif'>",
         f"<rect width='{W}' height='{H}' fill='#ffffff'/>",
         "<text x='24' y='32' font-size='18' font-weight='600' fill='#1f1f1f'>Constant WLab hue against constant CIELAB hue</text>",
         "<text x='24' y='54' font-size='13' fill='#5e5e5e'>Each row is one lightness, from gray (left) to the most vivid color that fits on screen. Each chip is split:</text>",
         "<text x='24' y='72' font-size='13' fill='#5e5e5e'>upper left, constant WLab hue; lower right, the same L* and C*ab at the CIELAB hue of the ringed chip,</text>",
         f"<text x='24' y='90' font-size='13' fill='#5e5e5e'>the {anchor}est of the most vivid. Where the halves differ, the two kinds of hue line disagree.</text>"]
    x = x0
    for P, pw, u in zip(planes, pws, used):
        o.append(f"<text x='{x}' y='{y0 - 26}' font-size='13' font-weight='600' fill='#1f1f1f'>WLab hue {P['H']:.0f}°</text>")
        o.append(f"<text x='{x}' y='{y0 - 9}' font-size='12' fill='#5e5e5e'>against CIELAB hue {P['hab']:.0f}°</text>")
        for k in range(nL):
            r = nL - 1 - k
            top = y0 if r == 0 else y0 + rowgap // 2 + r * (chip + rowgap)
            bot = y0 + ph if r == nL - 1 else y0 + rowgap // 2 + (r + 1) * (chip + rowgap)
            o.append(f"<rect x='{x}' y='{top}' width='{pw}' height='{bot - top}' fill='{hexc(P['bg'][:, k])}'/>")
        for i in np.flatnonzero(P['ok_w']):
            r = nL - 1 - int(round((P['Lg'][i] - P['Lv'][0]) / P['stepL']))
            c = int(round(P['Cg'][i] / P['stepC']))
            cx, cy = x + gap + c * (chip + gap), y0 + rowgap + r * (chip + rowgap)
            o.append(f"<path d='M{cx} {cy}H{cx + chip}L{cx} {cy + chip}Z' fill='{hexc(P['rgb_w'][:, i])}'/>")
            o.append(f"<path d='M{cx + chip} {cy}V{cy + chip}H{cx}Z' fill='{hexc(P['rgb_l'][:, i])}'/>")
            if not P['ok_l'][i]:
                o.append(f"<circle cx='{cx + chip * 0.72}' cy='{cy + chip * 0.72}' r='1.8' fill='#000000' fill-opacity='0.55'/>")
            if i == P['anchor']:
                o.append(f"<rect x='{cx - 1.5}' y='{cy - 1.5}' width='{chip + 3}' height='{chip + 3}' fill='none' stroke='#ffffff' stroke-width='2'/>")
        for c in range(0, u, 2):
            o.append(f"<text x='{x + gap + c * (chip + gap) + chip / 2}' y='{y0 + ph + 16}' font-size='11' text-anchor='middle' fill='#5e5e5e'>{int(c * P['stepC'])}</text>")
        o.append(f"<text x='{x + pw / 2}' y='{y0 + ph + 34}' font-size='12' text-anchor='middle' fill='#5e5e5e'>chroma (WLab)</text>")
        x += pw + sep
    for L in (10, 30, 50, 70, 90):
        r = nL - 1 - int(round((L - planes[0]['Lv'][0]) / planes[0]['stepL']))
        o.append(f"<text x='{x0 - 8}' y='{y0 + rowgap + r * (chip + rowgap) + chip / 2 + 4}' font-size='11' text-anchor='end' fill='#5e5e5e'>{L}</text>")
    o.append(f"<text x='{x0 - 40}' y='{y0 + ph / 2}' font-size='12' fill='#5e5e5e' transform='rotate(-90 {x0 - 40} {y0 + ph / 2})' text-anchor='middle'>lightness</text>")
    o.append(f"<text x='24' y='{H - 34}' font-size='12' fill='#5e5e5e'>CIE 1931 observer, D50 (the ICC profile connection space), shown through a Bradford adaptation to sRGB.</text>")
    o.append(f"<text x='24' y='{H - 16}' font-size='12' fill='#5e5e5e'>Each row sits on the gray of its own lightness. A dot marks a CIELAB half outside sRGB. Screen colors are approximate.</text>")
    o.append('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('hues', type=float, nargs='+', help='WLab hue angles in degrees')
    ap.add_argument('--anchor', choices=('dark', 'light'), default='dark')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    out = a.out or '../results/hue_planes_' + '_'.join(f'{int(h):03d}' for h in a.hues) + '.svg'
    P = [plane(h, a.anchor) for h in a.hues]
    open(out, 'w', encoding='utf8').write(svg(P, a.anchor))
    for p in P:
        g = p['gap'][p['ok_w'] & (p['Cg'] >= 10)]
        print(f'WLab hue {p["H"]:g}: anchor CIELAB hue {p["hab"]:.1f}; CIELAB hue of the WLab chips '
              f'(chroma 10 and up) {g.min():+.1f} to {g.max():+.1f} from the anchor')
    print(f'wrote {out}')
