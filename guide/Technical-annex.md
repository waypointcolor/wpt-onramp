# Technical annex: the equations behind Wpt and WLab

This annex states every equation the guide describes in words, with every constant, so the method can be reproduced without the code. It follows the 2015 Wpt and WLab papers (Derhak and Berns), and the companion package implements each equation in Octave, Python and a spreadsheet; section A.8 says where.

**Conventions.** Spectra are sampled from 380 to 780 nm in 5 nm steps. Wpt depends on the range and interval: the reference coordinates and every result here use this grid, and the base reflectances are interpolated to it with a cubic spline (and extrapolated outside their measured range). The workbooks take sample reflectances from 380 to 730 nm at 10 nm, interpolate them linearly to the 5 nm grid and hold the 730 nm value beyond it. The CIE tables are those of CIE 15 at 5 nm; the CIE 2015 functions are cut at 780 nm. D50 is computed from the CIE daylight components at 5000 K, as in the original Wpt code, rather than at the CIE's 5003 K; its white differs by less than 0.1 (Z = 82.47 against about 82.5). Color coordinates are column vectors. Angles are in degrees, and hue angles run from 0 to 360. A superscript + is the Moore–Penrose pseudoinverse.

## A.1 Sensor responses from spectra

For an observer with sensitivity functions C₁, C₂, C₃ (color-matching functions, cone fundamentals or camera sensor curves), a material with reflectance O and a light with spectral power L:

```latex
c_i = k \sum_{\lambda} C_i(\lambda)\, O(\lambda)\, L(\lambda), \qquad k = \frac{100}{\sum_{\lambda} C_2(\lambda)\, L(\lambda)}
```

The constant k makes the second response of a perfect white equal 100, which for XYZ is the usual Y = 100. Any other constant gives the same Wpt, because steps 2 and 4 of the normalization (A.3) rescale the lightness axis and the chromatic plane. The responses of a perfect white, O(λ) = 1, are written c\_w.

## A.2 CIELAB and ΔE00

CIELAB uses the tristimulus values X, Y, Z of the sample and Xn, Yn, Zn of white under the same light (CIE 15):

```latex
f(q) = \begin{cases} q^{1/3} & q > 0.008856 \\ 7.787\,q + 16/116 & \text{otherwise} \end{cases}
```

```latex
L^* = 116 f(Y/Y_n) - 16, \quad a^* = 500\,[f(X/X_n) - f(Y/Y_n)], \quad b^* = 200\,[f(Y/Y_n) - f(Z/Z_n)]
```

These are the classic CIE constants; WLab's lightness (A.5) uses the exact 6/29 form, which differs only for the darkest values. ΔE\*ab is the straight-line distance in CIELAB. ΔE00 follows CIE 142 as written out by Sharma, Wu and Dalal (2005).

## A.3 Wpt normalization

The Wpt normalization for one observing condition is a 3 × 3 matrix A, so that

```latex
\begin{bmatrix} W \\ p \\ t \end{bmatrix} = A\, c
```

It is built from the responses c\_w of white (A.1), the responses c\_j of the 40 base samples (j = 1 … 40) and their reference coordinates p\_j, t\_j (A.4), in four steps.

**Step 1: rotate white onto the first axis.** With Rᵈ(φ) the rotation by φ in the plane of axes d − 1 and d (cos φ at positions (d − 1, d − 1) and (d, d), −sin φ at (d − 1, d), sin φ at (d, d − 1)), rotate first in the plane of axes 2 and 3, then in the plane of axes 1 and 2:

```latex
R = R^{(2)}(\varphi_2)\, R^{(3)}(\varphi_3), \quad \varphi_3 = -\operatorname{atan2}(c_{w,3}, c_{w,2}), \quad \varphi_2 = -\operatorname{atan2}(c'_{w,2}, c'_{w,1})
```

Here c′\_w = R⁽³⁾(φ₃) c\_w. After R, white lies on the first axis. Any other rotation that takes c\_w onto the positive first axis gives the same A, because steps 3 and 4 absorb the difference.

**Step 2: set white to W = 100.**

```latex
M_1 = \operatorname{diag}\!\left(\frac{100}{(R\,c_w)_1},\, 1,\, 1\right) R
```

**Step 3: level the lightness.** With (u\_j, v\_j, z\_j) = M₁ c\_j, fit u\_j ≈ α₁ v\_j + α₂ z\_j + α₀ by least squares, then shear so the 40 samples of equal Munsell Value share one W:

```latex
M_2 = \begin{bmatrix} 1 & -\alpha_1 & -\alpha_2 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix} M_1
```

**Step 4: fit the hue and chroma plane to the reference.** With q\_j the second and third components of M₂ c\_j, collected as the 2 × 40 matrix Q, and P the 2 × 40 matrix of reference (p\_j, t\_j), with the columns of Q and P in the same sample order:

```latex
F = P\, Q^{+}, \qquad A = \begin{bmatrix} (M_2)_{\text{row }1} \\ F\, (M_2)_{\text{rows }2,3} \end{bmatrix}
```

A is linear and invertible, white always maps to (100, 0, 0), and every spectrally flat gray maps onto the W axis. If the observer is replaced by any invertible linear transform of itself (cone fundamentals in place of color-matching functions, say), A changes to absorb it and Wpt stays the same.

**Constant hue for a reflectance family.** Write a reflectance as a spectrally flat part a plus a scale b > 0 on a characteristic reflectance O\_c, so O(λ) = a + b O\_c(λ). Because A is linear and white maps to (100, 0, 0):

```latex
\begin{bmatrix} W \\ p \\ t \end{bmatrix} = a \begin{bmatrix} 100 \\ 0 \\ 0 \end{bmatrix} + b \begin{bmatrix} W_c \\ p_c \\ t_c \end{bmatrix}, \qquad h = \operatorname{atan2}(t_c, p_c)
```

Every member of the family has the same hue h, for every a and b, in every observing condition; h itself depends on the condition. WLab keeps the Wpt hue angle (A.5), so the family also shares one WLab hue. CIELAB applies its cube root to X, Y and Z separately, which breaks this: for one blue family (Munsell 5PB 5/6 with its minimum removed, a from 0 to 0.5, b from 0.3 to 1), the CIELAB hue spreads by 0.7° under D65 and 12.5° under illuminant A, while the Wpt hue is constant to 10⁻¹² (results/annex\_checks.log).

**Where the reference coordinates come from.** The reference p\_j, t\_j were fixed once, under the reference condition (CIE 1931 observer, illuminant C), by the original derivation in the Wpt paper. That derivation rounded the 40 samples onto a circle with an ellipse fit, turned the plane so the vivid yellow (Munsell 3.75Y 8/14) lies along +t with the reds on +p, and scaled the yellow to 100 from the W axis. Every condition, the reference included, now uses step 4 against those fixed values.

**Practical Wpt** (in preparation) uses base reflectances of the user's choosing, with their own Wpt coordinates under the reference condition as targets. Because those samples need not share one lightness, step 3 becomes a least-squares fit of the W row to each sample's own reference W, with white kept at 100; step 4 is unchanged.

## A.4 Reference coordinates of the 40 base samples

The base samples are the Munsell Renotation colors at Value 5 and Chroma 6, one per 2.5 hue steps, with reflectances from the Joensuu Munsell glossy spectral database (Kohonen, Parkkinen and Jääskeläinen 2006), corrected to the renotation under illuminant C (Derhak and Berns, Color Imaging Conference 2012). The 40 reflectances themselves are in the companion package (toolbox/wpt\_base\_munsell40.csv). Their reference p and t, used in step 4 of A.3, are listed below to four decimals; the companion package carries them to full precision (toolbox/wpt\_reference\_pt.csv). Under the reference condition all 40 have W = 19.77.

| Sample | p | t |
| --- | --- | --- |
| 2.5R 5/6 | 26.6958 | 10.9828 |
| 5R 5/6 | 26.0683 | 13.9781 |
| 7.5R 5/6 | 24.9609 | 16.6028 |
| 10R 5/6 | 22.9904 | 19.6855 |
| 2.5YR 5/6 | 20.1343 | 21.8139 |
| 5YR 5/6 | 16.4247 | 23.8841 |
| 7.5YR 5/6 | 12.7969 | 25.2459 |
| 10YR 5/6 | 7.9935 | 26.3794 |
| 2.5Y 5/6 | 3.0201 | 27.0055 |
| 5Y 5/6 | −1.7814 | 27.1721 |
| 7.5Y 5/6 | −6.2742 | 26.9339 |
| 10Y 5/6 | −10.1936 | 26.2080 |
| 2.5GY 5/6 | −14.5479 | 24.6226 |
| 5GY 5/6 | −18.3866 | 22.4503 |
| 7.5GY 5/6 | −22.6269 | 18.6105 |
| 10GY 5/6 | −24.9461 | 14.6733 |
| 2.5G 5/6 | −26.7275 | 9.3543 |
| 5G 5/6 | −27.1418 | 5.5268 |
| 7.5G 5/6 | −26.9935 | 2.6844 |
| 10G 5/6 | −26.4749 | −0.2369 |
| 2.5BG 5/6 | −25.7375 | −3.2592 |
| 5BG 5/6 | −24.4254 | −7.6296 |
| 7.5BG 5/6 | −23.2074 | −11.4475 |
| 10BG 5/6 | −20.8623 | −16.1647 |
| 2.5B 5/6 | −18.2867 | −19.7727 |
| 5B 5/6 | −14.6623 | −23.0722 |
| 7.5B 5/6 | −10.7502 | −25.2029 |
| 10B 5/6 | −6.7638 | −26.3787 |
| 2.5PB 5/6 | −2.1544 | −27.2297 |
| 5PB 5/6 | 2.4611 | −27.1365 |
| 7.5PB 5/6 | 8.2509 | −26.2136 |
| 10PB 5/6 | 13.2497 | −24.2460 |
| 2.5P 5/6 | 16.4446 | −21.1520 |
| 5P 5/6 | 19.2782 | −17.7135 |
| 7.5P 5/6 | 22.1595 | −13.1390 |
| 10P 5/6 | 24.1808 | −8.8070 |
| 2.5RP 5/6 | 25.6162 | −4.3832 |
| 5RP 5/6 | 26.6098 | 0.9937 |
| 7.5RP 5/6 | 27.0272 | 4.8202 |
| 10RP 5/6 | 26.9635 | 8.1618 |

**Relation to the 2015 Wpt paper.** The reference coordinates above are those of the Wpt toolbox and the companion package, and they are the canonical ones. The matrices published in the Wpt paper (its Table II), and the original Wpt normalization spreadsheet, use a slightly different reference, related to this one by

```latex
p_{2015} = 1.01125\, p, \qquad t_{2015} = t - 0.01331\, p
```

Applying this map to the reference coordinates reproduces the published matrices. White, the W axis and the vivid yellow at t = 100 are the same in both, and both sets of 40 samples are equally round (under the reference condition their chroma runs from 25.6 to 30.3, a standard deviation of about 4.5% of the mean). WLab values computed with the published matrices differ by at most 0.7 ΔE(WLab), mean 0.2, over 1,600 Munsell samples under D50 and D65 (results/annex\_checks.log). MATs and observer conversions are identical with either reference, because the map cancels between source and destination.

## A.5 WLab, forward and inverse

These are the equations of the WLab paper's appendix. Both directions use the same lightness and hue terms, so WLab converts back to Wpt exactly.

**Constants.** The implementations use the full-precision values; the paper prints them rounded. Over 1,600 Munsell samples (CIE 1931, D65) the rounded values change WLab by at most 0.05, mean 0.01 (results/annex\_checks.log).

| Constant | Value used | Published |
| --- | --- | --- |
| g₀ | 0.026742553710937 | 0.0267 |
| g₁ | 51.576165618406904 | 51.5762 |
| g₂ | 0.458886718750000 | 0.4589 |

**Wpt to WLab**

1. Lightness:

```latex
v = \begin{cases} (W/100)^{1/3} & W/100 > (6/29)^3 \\ \tfrac{1}{3}\left(\tfrac{29}{6}\right)^2 (W/100) + \tfrac{4}{29} & \text{otherwise} \end{cases}, \qquad L_w = 116\,v - 16
```

2. Chroma and hue of Wpt:

```latex
c_{pt} = \sqrt{p^2 + t^2}, \qquad h = \operatorname{atan2}(t, p) \in [0, 360)
```

3. Lightness dependence of chroma:

```latex
s = \frac{e^{\,g_0 (L_w - g_1)}}{g_2}, \qquad c_{mod} = \frac{c_{pt}}{s}
```

4. Hue terms:

```latex
r_1 = \begin{cases} \sin^3(h - 1) & 1 < h < 181 \\ 0 & \text{otherwise} \end{cases}, \quad r_2 = \begin{cases} 0.39 \cos^2(h - 14) & 104 < h < 284 \\ 0 & \text{otherwise} \end{cases}
```

```latex
d_0 = 62\,(r_1 + r_2 + 0.31), \qquad d_1 = 0.36\,(r_1 + r_2 + 0.19)
```

5. Chroma:

```latex
C_w = d_0 \left[ \ln\!\left(\frac{c_{mod}}{80} + d_1\right) - \ln d_1 \right]
```

6. Cartesian form: a\_w = C\_w cos h, b\_w = C\_w sin h. WLab is (L\_w, a\_w, b\_w); the hue angle h is unchanged from Wpt.

**WLab to Wpt.** Take C\_w and h from a\_w and b\_w, compute d₀, d₁ from h and s from L\_w as above, then:

```latex
c_{mod} = 80 \left[ e^{\,C_w / d_0 + \ln d_1} - d_1 \right], \qquad c_{pt} = s\, c_{mod}
```

```latex
v = \frac{L_w + 16}{116}, \qquad W = \begin{cases} 100\, v^3 & v > 6/29 \\ 300 \left(\tfrac{6}{29}\right)^2 \left(v - \tfrac{4}{29}\right) & \text{otherwise} \end{cases}
```

and p = c\_pt cos h, t = c\_pt sin h.

## A.6 ΔE(WLab)

```latex
\Delta E_{WLab} = \sqrt{(L_{w,1} - L_{w,2})^2 + (a_{w,1} - a_{w,2})^2 + (b_{w,1} - b_{w,2})^2}
```

The two WLab values may come from different observing conditions, since every condition goes through Wpt. ΔE(WLab) is a material color difference. For responses c in any condition, A c = A\_ref (A\_ref⁻¹ A c), and A\_ref⁻¹ A c is the MAT's prediction of the reference responses (A.7): Wpt in any condition is the reference condition's Wpt of what the reference observer (CIE 1931) is predicted to see under illuminant C. A ΔE(WLab) therefore estimates the color difference that observer would judge between the two materials under illuminant C. In the WLab paper's tests against two datasets from color-difference assessment experiments (CIE 1964 (10°) observer under D65 and illuminant A), it was not statistically different from ΔE94, ΔE00, DIN99o or CAM02-UCS. For large differences, the paper compared each space's lightness, chroma and hue with Munsell Value, Chroma and Hue over the Munsell colors (its Fig. 7): WLab tracks the Munsell system about as closely as CIELAB and CAM02-UCS do.

## A.7 Material adjustment transforms and observer conversion

**MAT.** With A\_src and A\_dst the Wpt normalizations (A.3) of a source and a destination observing condition, the MAT carries responses from one to the other through Wpt:

```latex
M_{src \rightarrow dst} = A_{dst}^{-1} A_{src}, \qquad c_{dst} \approx M_{src \rightarrow dst}\; c_{src}
```

White maps exactly: M c\_w,src = c\_w,dst. For other materials the result is a prediction; what is left over is their color inconstancy between the two conditions.

**Observer conversion.** Applied to the sensitivity functions themselves, at every wavelength, the same matrix gives a new set of functions that respond to materials as the destination observer does:

```latex
\mathbf{C}'(\lambda) = M_{src \rightarrow dst}\, \mathbf{C}_{src}(\lambda)
```

where **C**(λ) is the column of the three sensitivities at λ. Source and destination share the illuminant here. When the two observers are invertible linear transforms of each other, as cone fundamentals and color-matching functions of the same observer are, M equals that transform and the conversion is exact (to about 10⁻¹³ in the companion package). Between different observers it is a close fit for typical materials.

**For comparison, a CAT.** The von Kries-type CATs used in the companion package scale responses in a space S by the ratio of the two whites, with full adaptation:

```latex
M_{CAT} = S^{-1} \operatorname{diag}\!\left( \frac{S\, c_{w,dst}}{S\, c_{w,src}} \right) S
```

with S the Bradford or CAT02 matrix, or the identity for plain white scaling in XYZ. A CAT models one viewer adapting, so it is not designed to bridge two different observers.

The two matrices, from XYZ:

```latex
S_{Bradford} = \begin{bmatrix} 0.8951 & 0.2664 & -0.1614 \\ -0.7502 & 1.7135 & 0.0367 \\ 0.0389 & -0.0685 & 1.0296 \end{bmatrix}, \quad S_{CAT02} = \begin{bmatrix} 0.7328 & 0.4296 & -0.1624 \\ -0.7036 & 1.6975 & 0.0061 \\ 0.0030 & 0.0136 & 0.9834 \end{bmatrix}
```

## A.8 Where each equation is implemented

| Equations | Octave (toolbox/) | Python (wptonramp.py) | Spreadsheet |
| --- | --- | --- | --- |
| A.1 Sensor responses | ref2XYZ.m | ref2xyz | inputs are XYZ |
| A.2 CIELAB, ΔE00 | XYZ2Lab.m, deltaE00.m | xyz\_to\_lab, delta\_e00 | Calculator: L\*, a\*, b\*,\
ΔE\*ab, ΔE00 |
| A.3 Wpt normalization | getWptStruct.m | wpt\_normalization | Matrices sheet\
(14 conditions) |
| A.4 Reference p, t | wpt\_reference\_pt.csv | load\_base | — |
| A.5 WLab | Wpt2WLab.m, WLab2Wpt.m | wpt\_to\_wlab, wlab\_to\_wpt | Calculator\
(forward) |
| A.6 ΔE(WLab) | ex02, ex06 | delta\_e\_wlab | Calculator: ΔE(WLab) |
| A.7 MAT, CAT | ex05\_mats.m | mat | MAT sheet |

The three implementations agree to within 10⁻⁹ on the Wpt matrices and the spreadsheets, and to within 10⁻⁷ on WLab for 1,600 Munsell samples (the logs are in the package's results folder). Numbers in this annex that no example prints come from python/annex\_checks.py.
