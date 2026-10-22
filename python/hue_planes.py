"""Constant-hue planes in WLab and CIELAB, drawn as sRGB chips, to judge hue consistency for gamut mapping.

For a WLab hue angle h, chips are laid out with lightness up and chroma across, keeping only the
chips inside the sRGB gamut (CIE 1931 observer, D65). The CIELAB panel uses the CIELAB hue angle of
the lightest of the most chromatic WLab chips, so both planes pass through that colour. Along each
row the chips run from gray to the most vivid colour that fits: in a space whose hue lines suit
gamut mapping, they keep the same hue as they get more vivid.

    python hue_planes.py 288 --out ../results/hue_plane_288.svg

Writes an SVG; open it in a browser, or convert it to PNG. Screen colours are approximate.
"""

import argparse

import numpy as np

import wptonramp as w

M = np.linalg.inv(np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]))


def lab_to_xyz(lab, white):
    L, a, b = lab
    fy = (L + 16) / 116
    f = np.vstack([fy + a / 500, fy, fy - b / 200])
    t = np.where(f > 6 / 29, f ** 3, 3 * (6 / 29) ** 2 * (f - 4 / 29))
    return t * np.asarray(white).reshape(3, 1)


def srgb(xyz):
    lin = M @ (xyz / 100)
    ok = np.all((lin >= 0) & (lin <= 1), axis=0)
    g = np.clip(lin, 0, 1)
    g = np.where(g <= 0.0031308, 12.92 * g, 1.055 * g ** (1 / 2.4) - 0.055)
    return g, ok


def planes(h_deg, stepL=5, stepC=5):
    T = w.load_tables()
    n = w.wpt_normalization(T.observer['1931'], T.illuminant['D65'], w.load_base())
    white = w.ref2xyz(np.ones(len(T.nm)), T.observer['1931'], T.illuminant['D65'])[:, 0]
    Lv, Cv = np.arange(5, 96, stepL), np.arange(0, 91, stepC)
    Lg, Cg = (x.ravel() for x in np.meshgrid(Lv, Cv, indexing='ij'))
    h = np.radians(h_deg)
    xyz_w = n.wpt2xyz @ w.wlab_to_wpt(np.vstack([Lg, Cg * np.cos(h), Cg * np.sin(h)]))
    rgb_w, ok_w = srgb(xyz_w)
    i = np.flatnonzero(ok_w)
    i = i[Cg[i] == Cg[i].max()]
    i = i[np.argmax(Lg[i])]
    ref = w.xyz_to_lab(xyz_w[:, i], white)[:, 0]
    hab = np.degrees(np.arctan2(ref[2], ref[1])) % 360
    hb = np.radians(hab)
    xyz_l = lab_to_xyz(np.vstack([Lg, 2 * Cg * np.cos(hb), 2 * Cg * np.sin(hb)]), white)
    rgb_l, ok_l = srgb(xyz_l)
    # the gray of each row's lightness (the same in WLab and CIELAB, which agree on neutrals)
    bg, _ = srgb(n.wpt2xyz @ w.wlab_to_wpt(np.vstack([Lv, 0 * Lv, 0 * Lv]).astype(float)))
    return dict(Lv=Lv, Cv=Cv, Lg=Lg, Cg=Cg, w=(rgb_w, ok_w), l=(rgb_l, ok_l), hab=hab, bg=bg, stepC=stepC)


def svg(P, h_deg):
    hexc = lambda c: '#%02x%02x%02x' % tuple(int(round(255 * v)) for v in c)
    chip, gap, rowgap = 14, 2, 6
    nL, nC = len(P['Lv']), len(P['Cv'])
    used = max(int(P['Cg'][P['w'][1]].max() / P['stepC']), int(P['Cg'][P['l'][1]].max() / P['stepC'])) + 1
    pw, ph = used * (chip + gap) + gap, nL * (chip + rowgap) + rowgap
    W = max(760, 2 * pw + 260)
    x0s, y0 = (W // 2 - pw - 40, W // 2 + 80), 110
    H = y0 + ph + 90
    o = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}' font-family='Segoe UI, Helvetica, Arial, sans-serif'>",
         f"<rect width='{W}' height='{H}' fill='#ffffff'/>",
         f"<text x='24' y='32' font-size='18' font-weight='600' fill='#1f1f1f'>One hue from gray to vivid: WLab and CIELAB</text>",
         f"<text x='24' y='54' font-size='13' fill='#5e5e5e'>Each row is one lightness. Chips run from gray (left) to the most vivid color that fits</text>",
         f"<text x='24' y='72' font-size='13' fill='#5e5e5e'>on screen (sRGB). For gamut mapping, a row should keep one hue as it gets more vivid.</text>"]
    for p, (key, title, sc, xl) in enumerate((('w', f'WLab, hue {h_deg}°', 1, 'chroma (WLab)'),
                                               ('l', f'CIELAB, hue {P["hab"]:.0f}°', 2, 'chroma C*ab'))):
        x0 = x0s[p]
        rgb, ok = P[key]
        o.append(f"<text x='{x0}' y='{y0 - 12}' font-size='14' font-weight='600' fill='#1f1f1f'>{title}</text>")
        for k in range(nL):
            r = nL - 1 - k
            top = y0 if r == 0 else y0 + rowgap // 2 + r * (chip + rowgap)
            bot = y0 + ph if r == nL - 1 else y0 + rowgap // 2 + (r + 1) * (chip + rowgap)
            o.append(f"<rect x='{x0}' y='{top}' width='{pw}' height='{bot - top}' fill='{hexc(P['bg'][:, k])}'/>")
        for i in np.flatnonzero(ok):
            r = nL - 1 - int(round((P['Lg'][i] - P['Lv'][0]) / 5))
            c = int(round(P['Cg'][i] / P['stepC']))
            o.append(f"<rect x='{x0 + gap + c * (chip + gap)}' y='{y0 + rowgap + r * (chip + rowgap)}' width='{chip}' height='{chip}' fill='{hexc(rgb[:, i])}'/>")
        for L in (10, 30, 50, 70, 90):
            r = nL - 1 - int(round((L - P['Lv'][0]) / 5))
            o.append(f"<text x='{x0 - 8}' y='{y0 + rowgap + r * (chip + rowgap) + 11}' font-size='11' text-anchor='end' fill='#5e5e5e'>{L}</text>")
        o.append(f"<text x='{x0 - 40}' y='{y0 + ph / 2}' font-size='12' fill='#5e5e5e' transform='rotate(-90 {x0 - 40} {y0 + ph / 2})' text-anchor='middle'>lightness</text>")
        for c in range(0, used, 2):
            o.append(f"<text x='{x0 + gap + c * (chip + gap) + chip / 2}' y='{y0 + ph + 16}' font-size='11' text-anchor='middle' fill='#5e5e5e'>{int(c * P['stepC'] * sc)}</text>")
        o.append(f"<text x='{x0 + pw / 2}' y='{y0 + ph + 36}' font-size='12' text-anchor='middle' fill='#5e5e5e'>{xl}</text>")
    o.append(f"<text x='24' y='{H - 30}' font-size='12' fill='#5e5e5e'>Each row sits on the gray of its own lightness. CIE 1931 observer, D65. Both planes pass through</text>")
    o.append(f"<text x='24' y='{H - 12}' font-size='12' fill='#5e5e5e'>the lightest of the most vivid WLab chips. Screen colors are approximate.</text>")
    o.append('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('hue', type=float, help='WLab hue angle in degrees')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    h = int(a.hue) if a.hue == int(a.hue) else a.hue
    out = a.out or f'../results/hue_plane_{int(a.hue):03d}.svg'
    P = planes(a.hue)
    open(out, 'w', encoding='utf8').write(svg(P, h))
    print(f'wrote {out}; CIELAB hue {P["hab"]:.1f}; chips WLab {P["w"][1].sum()}, CIELAB {P["l"][1].sum()}')
