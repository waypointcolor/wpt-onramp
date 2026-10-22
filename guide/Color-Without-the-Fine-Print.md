# Color Without the Fine Print: An Onramp to Wpt, WLab, and Material Color Equivalency

Oct 21, 2026 · @Max

## Why this guide exists

This guide is an onramp to a different way of describing color: by the *material* (a paint, an ink, a fabric, a plastic) rather than by how it measures under one light for one viewer. It ends at two coordinate systems, Wpt (pronounced "Waypoint") and WLab, introduced properly once the groundwork is in place.

Most people who work with color are at least familiar with the CIELAB color coordinate system and the ΔE color difference score. Both are good tools. But they answer a narrower question than most people think. This guide shows what that question is and what Wpt and WLab add.

No math is needed to follow the ideas. The few formulas are optional, and each one comes with a plain-words version.

For readers who want the full method, every equation and constant is written out in the Technical annex.

**Pick your path**

- New to color numbers: read straight through.
- Comfortable with Lab and ΔE: skim "What you already know", then read on from "The three ingredients of every color".
- Buying or managing color: read "A material does not have one Lab value", then "For buyers and managers".
- Want to use it now: read "When to reach for Wpt and WLab", then "Getting started".

## The short version

- A CIELAB value describes a sample under one light, as one standard viewer sees it. Change the light or the viewer and the value changes, by a different amount for each sample.
- That is why two samples that match in the viewing booth can stop matching in the store. The name for it is metamerism.
- Wpt and WLab are coordinates for the material itself: they stay nearly the same whatever the light and whoever is looking. WLab differences are similar in size to ΔE00 values.
- With them you can ask questions a booth reading cannot answer. Will this match hold under store lighting? Does this ink hold its color? Do these two viewers, or a camera and a person, agree?
- A material adjustment transform (MAT) carries measurements from one light or viewer to another by way of the material.
- Keep CIELAB and ΔE00 for work under one light and for contracts. Reach for WLab when a comparison crosses lights, viewers or devices.

The rest of this guide explains each of these, with a worked example.

## What you already know: CIELAB and ΔE

A CIELAB value is the color of a sample as one standard viewer sees it under one named light. Everything else in this guide builds on that one sentence.

CIELAB gives each color three numbers:

- **L\*** is lightness, from 0 (black) to 100 (white).
- **a\*** runs from green (negative) to red (positive).
- **b\*** runs from blue (negative) to yellow (positive).

**ΔE** is how far apart two colors sit in that space. ΔE\*ab is the plain straight-line distance. CIEDE2000 (ΔE00) adds corrections for regions where the straight line gets it wrong, such as blues and near-neutrals. As a rough guide, a ΔE00 near 1 is a difference a trained eye can just see side by side.

**How a Lab value is made**

1. Measure the sample's spectral reflectance: how much light it reflects at each wavelength.
2. Choose an observer (the CIE 2° or 10° standard observer) and an illuminant (often D50 or D65).
3. Combine the three to get tristimulus values, X, Y and Z.
4. Divide by the X, Y and Z of white under the same light.
5. Compress the result with a cube-root curve and apply some math to get L\*, a\* and b\*.

**The assumptions behind it**

- **The light is fixed.** A value marked "D50, 2°" holds for D50 only. Under a tungsten lamp the sample has a different Lab value.
- **The viewer is an average.** The standard observers are averages from color-matching experiments run in the 1920s to 1950s. No real person matches them exactly, and no camera does.
- **Dividing by white only lines up the neutrals.** Step 4 makes white and grays agree from one light to the next. It does not do the same for reds, greens or blues.

None of these is a flaw when you stay in one condition. They matter as soon as you compare across lights or viewers, which real work keeps doing.

## The three ingredients of every color

Every color measurement combines three things: a light, a material and an observer. Change any one of them and the numbers change.

- **The light** (illuminant) has a spectrum: how much power it gives at each wavelength. Daylight, tungsten, fluorescent and LED lights all have different spectra.
- **The material** has a spectral reflectance: the fraction of light it sends back at each wavelength. This belongs to the object. It is the part people usually mean by "the color of the paint".
- **The observer** has three sensitivity curves. For a person these are the three cone types, or the color-matching functions of a standard observer. For a camera they are its red, green and blue sensor curves.

Let's think of the combination of the observer and the light together as an **observing condition**. That is broader than the usual "viewing condition", which tends to mean only the light.

Each of the observer's three responses is built up wavelength by wavelength: how much light the source gives, times how much the material reflects, times how sensitive that sensor is, all added together.

**An analogy.** Think of the material as a song, the light as the room it is played in and the observer as the listener's ears. A CIELAB value is a recording of what one standard listener heard in one room. The rest of this guide is about writing down the song itself, as far as three numbers can.

## A material does not have one Lab value

Many people believe a swatch *is* its Lab value. It is not. A Lab value describes one swatch under one light for one observer, and changing the light or the observer changes it, by a different amount for each swatch.

Three everyday effects come out of this:

- **Metamerism.** Two materials with different spectra match under one light and not under another. Two gray fabrics match in the store and look different outdoors.
- **Observer metamerism.** Two people, or a person and a camera, disagree about whether two samples match. Displays with narrow-band primaries are known for this.
- **Color inconstancy.** One material's color shifts, relative to typical materials around it, when the light or the observer changes.

**A worked example.** Take one patch of the X-Rite ColorChecker, Purplish Blue, and its twin from the MetaChecker, a research set of computed spectra made to match each ColorChecker patch. The twin has a deliberately jagged spectrum that matches the real patch exactly for the CIE 1931 (2°) standard observer under D65. View both under D65, then under illuminant A, a tungsten-like light.

&#91;embedded content: ColorChecker and MetaChecker reflectances; CIE illuminants D65 and A · 380–730 nm in 5 nm steps\]

The two spectra look nothing alike, yet under D65 they give exactly the same numbers. The twin reflects a lot of red light, and illuminant A is rich in red light, so under A the twin turns redder than the real patch.

| Purplish Blue | Real ColorChecker patch\
(smooth spectrum) | MetaChecker twin\
(jagged spectrum) |
| --- | --- | --- |
| CIELAB under D65 | 41.7, 14.4, −42.9 | 41.7, 14.4, −42.9 |
| CIELAB under A | 39.2, −1.9, −45.5 | 39.1, 25.1, −48.7 |
| Change from D65 to A, ΔE00 | 12.7 | 5.4 |

Under D65 the two are a perfect match. Under A they are ΔE00 17.3 apart: that is metamerism. CIELAB also says the real, smooth-spectrum patch changed more than its jagged twin. Is that true of the materials?

Not from plain CIELAB. Dividing by white (step 4 above) is a rough stand-in for the eye adapting to the light: it is exact for grays and only approximate for everything else. So a plain CIELAB change from one light to another mixes what the material does with what that rough step misses. The rest of this guide comes back to this example once the pieces are in place.

*These values were calculated for this guide with the CIE 1931 observer. They are not a visual experiment.*

## Material Color Equivalency: same stuff, not same look

There are two different ways for colors to be "the same". Color science has long mixed them up, and the coordinates in the rest of this guide are built on the second one.

Tear a sheet of paper in half. Put one half under daylight and the other under a warm tungsten lamp. Then ask two different questions:

- **Do they look the same?** Usually not quite: the tungsten half looks warmer. Asking which patch under tungsten *looks like* the daylight half gives **corresponding colors**. That is the ground truth behind chromatic adaptation transforms (CATs) and color appearance models such as CIECAM02 and CAM16.
- **Are they the same material?** Yes, and people can judge this to some degree, even when the two halves look different. Asking which patch under tungsten is *made of the same stuff* is the idea behind experiments where people pick the **least dissimilar match**: the patch that differs least from the original when none matches exactly. Colors judged to be the same material belong to one **material color equivalency (MCE)** class.

A material match involves all three ingredients together: the material, the light and the observer. A good material coordinate should stay roughly the same whichever light the material is under and whoever is looking. (For the research behind this idea, see "The idea of material color" under Further reading.)

**A waypoint for color.** A waypoint is a fixed reference point on a route that you navigate by. A material color equivalency space can play that role between observing conditions: go from where you are into the shared space, then out to where you want to be. The next section builds such a space and names it for this idea: Wpt, pronounced "Waypoint".

Keep the two ideas side by side, not in competition. Appearance answers "what will this look like here?" Material equivalency answers "is this the same material, and how far apart are these materials?" They are complementary, and one can feed the other.

## Wpt: coordinates for the material

**Wpt normalization** turns an observer's three responses into three material coordinates, W, p and t. It is a short series of basic math steps (rotate, tilt, stretch and scale), worked out once for each observing condition. The steps are chosen so that the same materials land in nearly the same place whatever the light and observer. (Mathematically, the steps combine into one 3 × 3 matrix, but you don't need to know that to use it.)

**The three axes**

| Axis | Meaning | Direction |
| --- | --- | --- |
| W | Lightness | White = 100, black = 0 |
| p | First opponent axis | Reddish toward +p, greenish toward −p |
| t | Second opponent axis | Yellowish toward +t, bluish toward −t |

The layout echoes CIELAB on purpose: W is like L\*, p like a\*, and t like b\*. Unlike CIELAB, Wpt uses no curves: each coordinate is a weighted mix of the three responses. That is why it works the same way from XYZ, cone responses or camera RGB.

**How the normalization is built (optional reading)**

The Munsell system is a color atlas laid out in equal visual steps of hue, lightness (Value) and colorfulness (Chroma); "5R 5/6" means hue 5R, Value 5, Chroma 6. Wpt's reference is the Munsell Renotation, with the CIE 1931 (2°) observer under illuminant C, an older daylight standard. Forty Munsell colors at Value 5 and Chroma 6 cover every hue at one lightness and one chroma. A perfect white and one vivid yellow (Munsell 3.75Y 8/14, close to unique yellow) complete the set of 42, shown below.

&#91;image: The 42 samples that set up Wpt: white, 40 Munsell hues at Value 5, Chroma 6, and a vivid yellow\]

*All 40 hues share one Munsell Value (lightness) and one Chroma (colorfulness); only the hue changes. On screen they may not look equally vivid, because the swatches are approximate renderings.*

From these samples, the reference normalization is built in five steps:

1. **Line up white.** Rotate the space so white lies on the first axis, and scale it so white has W = 100. Every neutral now sits on the W axis.
2. **Level the lightness.** Tilt the space so the 40 colors of equal Munsell Value share one W.
3. **Round the chroma.** Stretch the chromatic plane so the 40 colors of equal Munsell Chroma sit on a circle.
4. **Point the hues.** Turn the circle so the vivid yellow points along +t and the reds fall on +p.
5. **Set the scale.** Scale p and t so the vivid yellow is 100 from the W axis.

This gives the reference normalization. For any other observer or light, steps 1 and 2 are repeated, and a best-fit step then moves the 40 colors as close as it can to where they sit in the reference. The fit works in order: white first, then lightness, then hue and chroma. It decides what to keep exact and where the compromises go.

Practical Wpt keeps that reference and lets you choose which materials carry it to a new condition, such as the patches of a ColorChecker or a set of inks. The reference itself never moves.

**Properties worth knowing**

- **Neutrals are exact.** A spectrally flat gray has the same Wpt under every light and for every observer.
- **The form of the observer doesn't matter.** Color-matching functions, cone fundamentals or any other re-mix of the same observer's curves give identical Wpt coordinates.
- **It is invertible.** Every normalization can be run backwards, from Wpt to that condition's XYZ, cone values, or sensor values.
- **A material's tints and shades keep one hue.** Combine a material's reflectance with a spectrally flat gray in any proportion, and every result has exactly the same Wpt hue, under any light and for any observer. That hue can move a little from one condition to another, but within each condition the whole family shares it. CIELAB does not do this: for one blue family, its hue spread by up to 12° under tungsten light.
- **It is not perceptually uniform.** Equal steps in Wpt are not equal visual steps. That is WLab's job.

## WLab: measuring difference between materials

WLab (Waypoint-Lab) reshapes Wpt so that a plain straight-line distance works as a color difference, comparable to the leading ΔE formulas. Like those CIELAB-based formulas, it corresponds to perceived color differences under a reference observing condition. WLab is not a color appearance space. It is to Wpt what CIELAB is to XYZ.

WLab has three coordinates, Lw, aw and bw, read like L\*, a\* and b\*. The difference between two colors, ΔE(WLab), is just the straight-line distance between them, as ΔE\*ab is in CIELAB.

**What the transform does, in words (optional reading)**

1. **Lightness.** W goes through the same cube-root curve that CIELAB uses for L\*, so Lw reads like L\*.
2. **Chroma and lightness.** Chroma is rescaled with lightness, so a given chroma means the same at light and dark levels.
3. **Chroma and hue.** Chroma is compressed on a logarithmic curve whose strength depends on hue. This is the step that makes small and large differences come out right together.

Each step can be undone, so WLab converts back to Wpt exactly. The equations take a few more lines than CIELAB's and are about as involved as CIEDE2000's. The difference is where the work happens: CIEDE2000 adds weights every time two colors are compared, while WLab puts the work into the coordinates once, so every comparison afterwards is a straight line.

**How good is it?** Tested against standard visual color-difference data, ΔE(WLab) did statistically as well as ΔE94, ΔE00 and other leading formulas. Against the Munsell system, its large-scale spacing is about as even as CIELAB's and CAM02-UCS's. The details are in the Technical annex (A.6).

**What a WLab difference means.** Because every WLab value goes through Wpt, a ΔE(WLab) is a difference between *materials*, not between two appearances. Values from different lights and observers share one common representation, so you can compare them directly, the way prices compare once they're all in the same currency. That includes custom observers, not only the CIE standard ones: the CIE 2006 observers for a given age and field size, the CIE 2015 observers, or a camera's sensor curves. Build the Wpt normalization for that observer and light, and its WLab values join the same representation. That lets us finish the Purplish Blue example.

**The example, revisited.** Here are the same two Purplish Blue patches from "A material does not have one Lab value", now in WLab.

| Purplish Blue | Real ColorChecker patch\
(smooth spectrum) | MetaChecker twin\
(jagged spectrum) |
| --- | --- | --- |
| WLab under D65 | 41.7, 10.3, −32.2 | 41.7, 10.3, −32.2 |
| WLab under A | 42.2, 8.0, −32.1 | 39.9, 21.1, −32.2 |
| Change from D65 to A, ΔE(WLab) | 2.3 | 11.0 |
| CIELAB change, for comparison, ΔE00 | 12.7 | 5.4 |
| CIELAB with a CAT (CAT02),\
change, ΔE00 | 0.9 | 14.1 |

WLab reverses plain CIELAB's verdict: the real patch with its smooth spectrum barely moves, and the jagged twin moves a lot. Across the 18 chromatic ColorChecker patches, plain CIELAB says the real patch moved more than its twin in 5 cases; WLab says so in none.

The last row shows that the familiar fix agrees. Adding a proper chromatic adaptation step to CIELAB (CAT02, described under "CATs and MATs") gives the same verdict for this single observer. What WLab adds is one common representation in which the same comparison also works across observers and cameras, and an adjustment built on materials rather than on how colors look. What a material moves beyond typical materials is its color inconstancy.

**One caution.** ΔE(WLab) does not predict what a particular person will see in a particular room. That is the job of a color appearance model. WLab tells you how far apart materials are, in units that behave like familiar ΔE units.

**Where it all fits.** Each column pairs a simple, curve-free space with its more uniform partner, the way XYZ pairs with CIELAB.

&#91;embedded content: where Wpt and WLab sit among familiar color spaces · 3 columns, 2 rows\]

Read across a row to compare the kinds of question each space answers; read down a column to see the uniform space built on its curve-free base.

## CATs and MATs: two ways to bridge conditions

**Start with the familiar one: the CAT.** A chromatic adaptation transform (CAT) predicts which numbers will *look the same* to one viewer after the light changes. Your eyes adapt: a white shirt still looks white under a warm lamp. A CAT models that adaptation. It is built from corresponding-color experiments, in which people match how colors look under two different lights. CATs such as Bradford and CAT02 are used widely in color management and sit inside color appearance models such as CIECAM02 and CAM16.

**Now the new idea: the MAT.** A material adjustment transform (MAT) asks a different question: what will this *same material* measure under a different light, for a different observer, or both? It does not model a viewer adapting. It predicts the numbers the material itself would give in the new condition, as if you had measured it there.

Think back to the torn sheet of paper. A CAT asks which patch under tungsten *looks like* the daylight half. A MAT asks what the tungsten half of the same sheet will measure. The two answers usually differ.

**When you want a MAT.** Whenever the material is what matters:

- converting measurements made under one light to another light;
- converting a camera's, or a particular person's, responses to standard colorimetry, and back;
- comparing data gathered for different observers.

In each case there is no single adapted viewer to model, only a material and the numbers it would give. Because a MAT works through materials, it handles a change of observer as easily as a change of light. A CAT is not designed to bridge two different observers. It describes how one viewer adapts to a new light, and says nothing about how two viewers' responses relate. Even so, CATs often get used for these jobs, simply because they are the familiar tool.

**No MAT is exact.** A material's numbers in a new condition depend on its full spectrum, and three numbers do not record a spectrum. The Purplish Blue twins prove it: identical numbers under D65, different numbers under A. A MAT makes the best prediction for typical materials. What is left over is the color inconstancy that WLab measures.

**Converting the observer itself.** A MAT can be applied to more than measurements. Apply it to an observer's sensitivity curves (cone fundamentals, color-matching functions or camera sensor curves) and you get a new set of curves that responds to materials the way the destination observer does. For example:

- cone fundamentals to color-matching functions;
- the CIE 2015 observer to the CIE 1931 observer;
- a camera's sensors to a standard observer.

Material equivalency is what makes this work: the converted curves put each material where the destination observer would put it. For two forms of the same observer, such as its cone fundamentals and its color-matching functions, the conversion is exact. Between different observers it is the best fit for typical materials. This is a powerful new tool: it lets custom observers, cameras and the standard observers share one color-managed workflow.

Both work the same way: go into an intermediate space, then come out again. Even the white balance in a camera works this way: it scales the colors so the scene's white becomes a standard white, then scales them again for the white you want to show. What differs is the waypoint in the middle:

- A **CAT** goes through sharpened cone responses divided by white, tuned to corresponding-color experiments. Its waypoint keeps *appearance*.
- A **Wpt MAT** goes through Wpt. Its waypoint keeps *material*. The whole MAT is two steps.

First, the source condition's Wpt normalization takes you into Wpt. Then the destination's normalization, run backwards, takes you out.

&#91;embedded content: CAT and MAT routes · same shape, different waypoint\]

The shape of the route is the same; what the middle step is built to keep is what differs.

|  | Chromatic adaptation\
transform (CAT) | Material adjustment\
transform (MAT) |
| --- | --- | --- |
| Question | What looks the same to this\
viewer under the new light? | What will this material measure\
under the new light or observer? |
| Built from | Corresponding-color\
experiments | Materials (Munsell reference, or\
a chosen set of base reflectances) |
| Handles a change\
of observer | No: it models one\
viewer adapting | Yes: light, observer\
or both in one step |
| White and grays | Mapped exactly\
(with full adaptation) | Mapped exactly |
| Typical use | Appearance, color\
appearance models | Converting measurements,\
custom observers,\
comparing conditions |

**Does it work?** Over 5,162 real reflectances (flowers, ColorChecker charts, Munsell, natural objects, paper, lumber, IT8 targets; the set includes Munsell samples of the kind Wpt is built from), the Wpt MAT predicted D65 colorimetry from other conditions more closely than CAT02 or an earlier published MAT did. For the 10° observer the mean ΔE00 from illuminant A was 1.24 for the Wpt MAT against 2.35 for CAT02. As you would expect, CAT02 predicts corresponding colors better than the MAT does. Each is best at its own job.

The two also chain together: a MAT can bring measurements to a standard condition, and a CAT or color appearance model can take over from there.

## What you can do with it

WLab values from any material, light and observer share one common representation. That turns several hard questions into the same simple move: hold some of the three ingredients fixed, vary the rest, and measure the distance in WLab.

| Question | What changes\
(what stays fixed) | What the WLab distance\
tells you |
| --- | --- | --- |
| How different are\
these two samples? | The material\
(light and observer fixed) | Color difference,\
as with ΔE |
| Does this sample\
hold its color? | Light, observer or both\
(one material) | Color inconstancy: how far\
the material moves from itself |
| Will this match\
survive? | Light, observer or both\
(two materials that match\
in one condition) | Metamerism: how far\
apart they drift elsewhere |
| Do these two\
observers agree? | The observer: a person,\
a standard or a camera\
(materials and light fixed) | Observer equivalency:\
how alike two observers are |
| How well does this\
light render color? | The light\
(materials and observer fixed) | Illuminant color rendering\
against a reference light |
| All of the above\
at once | Several things | Combinations, such as\
a camera under LED against\
a person in daylight |

One caution for the observer and light rows: each Wpt normalization is the best simple fit for its condition, so these numbers measure what is left after the best simple adjustment between two conditions. They show how differently materials behave, not overall shifts such as a light that makes every color a little more vivid.

**Shift manifolds.** One material under many lights and observers gives a small cloud of Wpt points, its *Wpt shift manifold*. The cloud's size shows how inconstant the material is, and its shape shows which way it drifts. Research metrics built on these clouds are listed under Further reading. Materials whose spectra have similar overall shapes tend to drift alike.

**Conversions.** A MAT is also a practical tool:

- **Between observers.** Convert colorimetry for a custom observer (one person, an age group, a camera) to and from standard colorimetry. It works the same whether the observer is given as cone fundamentals or color-matching functions.
- **Between lights.** Estimate what a measurement taken under one light would be under another when no spectral data are available.
- **In color management.** iccMAX profiles can carry a Wpt MAT, so custom-observer workflows run in an ordinary color-managed pipeline. The open-source iccDEV implementation does this.

**Another option to try: gamut mapping.** Every printer and display can reproduce only part of the full range of colors, its *gamut*. Gamut mapping moves colors that fall outside it to ones that fit, usually toward gray while trying to keep their hue. WLab can serve as the space for that mapping. A line of constant WLab hue is a straight line out from white on the familiar horseshoe-shaped chromaticity diagram, and distances work like familiar ΔE color differences. A straight line on that diagram is not exactly constant perceived hue, especially among the blues, so how well it works depends on the printer, the display and the images. Wpt has been used for gamut mapping with reasonable results; it is an option to try and judge on your own work.

You can judge the hue lines by eye. The picture shows one blue in both spaces, from gray to the most vivid color a screen can show. Compare each row: as the chips get more vivid, CIELAB's blues drift from violet toward azure more than WLab's do. The companion package draws the same picture for any hue.

&#91;image: One blue hue from gray to vivid, in WLab and in CIELAB, each row on the gray of its own lightness\]

## When to reach for Wpt and WLab

If everything happens under one light for one standard observer, CIELAB and ΔE00 are fine; keep using them. Reach for Wpt and WLab when a comparison crosses lights, observers or devices.

| Your situation | Use |
| --- | --- |
| Checking a print against a proof\
in one viewing booth | CIELAB and ΔE00 |
| A specification or contract\
written in ΔE00 | CIELAB and ΔE00 |
| Judging whether a match will hold\
under store, office and home lighting | WLab: metamerism and\
color inconstancy |
| Comparing data measured under\
different lights or for\
different observers | Wpt and WLab: one common\
representation for all of it |
| Converting colorimetry between\
a custom observer, a camera\
and a standard observer | A Wpt MAT |
| Describing colors and color differences\
for a custom observer (an age group,\
a CIE 2015 observer, a camera) | Wpt and WLab built\
for that observer |
| Choosing between lights, or between\
materials, for consistent color | WLab across the candidates |
| Predicting how a scene will look\
to a viewer adapted to its surroundings | A color appearance model\
(CIECAM02 or CAM16),\
optionally fed by a MAT |

**What not to expect.** Wpt reduces color inconstancy; it does not remove it. A material with a jagged spectrum will still drift, and WLab will show it drifting. That is information, not error. And over one chart, Wpt gives essentially the same answer as a least-squares fit that keeps white exact. Its value is the one common, meaningful representation it gives you, not extra accuracy over regression.

## For buyers and managers

You will rarely compute WLab yourself. As with ΔE today, you ask for it, read it and decide. What it adds is the question a booth ΔE cannot answer: will this match hold where the product is actually seen?

**A story.** A brand owner approves a red. Two suppliers submit matches, and both measure ΔE00 0.0 against the standard in the D50 viewing booth. Both pass. A WLab robustness report then compares each submission with the standard under the other lights the product will meet:

| Light (observer) | Submission 1 (smooth) | Submission 2 (jagged) |
| --- | --- | --- |
| D50 booth, ΔE00 | 0.0 | 0.0 |
| D50 booth | 0.0 | 0.0 |
| D65 daylight | 0.0 | 0.5 |
| A, home tungsten | 0.1 | 0.7 |
| F2, cool white fluorescent | 0.5 | 3.7 |
| F11, tri-band store fluorescent | 0.9 | 12.9 |
| D50, CIE 1964 (10°) observer | 0.1 | 0.2 |

All values are ΔE(WLab) against the standard, CIE 1931 observer, except where the row says otherwise. Submission 1 stays close everywhere. Submission 2 matches in the booth but drifts apart under fluorescent store lighting. If the product will sit under that kind of light, Submission 1 is the safer choice, even though both passed.

*The three spectra were made for this guide from a Munsell red included in the companion package, so the example can be rerun. Real submissions made with very different colorants can behave like Submission 2.*

**What to ask for**

- Spectral reflectance of the standard and of each submission or production sample, not just Lab values: for example 400–700 nm or wider, every 10 nm or finer.
- The lights that matter for the product: the viewing booth, the store lighting and home lighting. For a particular store light, its measured spectrum.
- A robustness report: ΔE(WLab) between each sample and the standard under each of those lights, and for a second observer if viewers of different ages matter.

Sample wording for a request: *"With each submission, supply the spectral reflectance of the submission and the standard (400–700 nm at 10 nm or finer), and a WLab robustness report against the standard under D50, illuminant A and our store lighting, CIE 1931 observer."*

If the spectra come to you, you can make the report yourself: the companion package includes a robustness workbook. Paste the spectra of the standard and up to ten samples, pick the lights from a list, and the table above appears. Your own store or home lights can be added by pasting their measured spectra. It needs no programming.

**How to read the report**

- Read each number like a ΔE: ΔE(WLab) values are similar in size to ΔE00 values.
- There is no universal tolerance, just as ΔE00 and ΔE\*ab tolerances differ from one industry to the next. Let experience with your own products set the limits, and keep your booth ΔE00 specification as it is.
- Look for patterns more than single numbers. A submission that stays small under every light is robust; one that jumps under one kind of light is a metamerism risk under that light.

**Decisions it supports**

- Choosing between submissions, suppliers or formulations that all pass in the booth.
- Knowing in advance which lights are likely to cause complaints, and setting expectations with the brand owner.
- Keeping parts made of different materials consistent under the lights where they are seen together.
- Choosing store lighting that keeps brand colors steady.

## Getting started

If you can compute CIELAB from a spectrum, you can compute WLab: it is one extra normalization step and one short function. Here is the recipe, followed by a quick check that you got it right.

**With spectral measurements**

1. Measure the spectral reflectance of your samples.
2. List the observing conditions you care about, for example CIE 1931 under D65, under illuminant A and under the LED in your store.
3. For each condition, compute X, Y and Z (white has Y = 100), then apply that condition's Wpt normalization to get W, p and t.
4. Convert Wpt to WLab.
5. Measure distances as in the table in "What you can do with it".

**With colorimetry only.** If you have XYZ for one known condition but no spectra, a MAT estimates the XYZ for another: apply the source condition's normalization, then the destination's run backwards. The companion package lists ready-made normalizations for the CIE 2° and 10° observers under C, D50, D65, A, E, F2 and F11. The Wpt paper's published matrices use a slightly different reference; the Technical annex explains how they relate.

**Sanity checks**

- A spectrally flat 50% gray gives WLab (76.1, 0, 0) under every light, the same as its L\*.
- Lw lands close to CIELAB L\*: for ColorChecker patches under D65 the two agree to within about 0.5. They are identical under the reference condition (CIE 1931, illuminant C), and can differ by several units under tungsten-like light A.
- Recompute the Purplish Blue example earlier in this guide. If your numbers match it, your pipeline is right.

**Tools**

- **Companion package.** Every example in this guide comes with code you can run and change: GNU Octave (or MATLAB) scripts, the same examples in Python, and an Excel calculator for XYZ to Wpt, WLab and CIELAB, the three color differences, and MATs. All three give the same numbers, and each example is a starting point for your own. It also includes a robustness workbook, with no programming needed, that turns measured spectra into a table like the one in "For buyers and managers", and a Wpt normalization workbook that shows the four steps and builds MATs for any observer and light.
- **iccMAX.** The open-source [iccDEV](https://github.com/InternationalColorConsortium/iccDEV) tools build and apply profiles that carry a Wpt MAT for custom observers.

Open question: where the companion package will be published.

## Glossary

| Term | Plain meaning |
| --- | --- |
| CAT\
(chromatic adaptation transform) | Predicts which numbers will look the same\
to one viewer under a different light |
| CIELAB (L\*, a\*, b\*) | The standard coordinates for a color\
under one light for one standard observer |
| CIE 1931 (2°) and\
CIE 1964 (10°) observers | The two standard observers: averages of\
people's color matching, for a small and\
a larger field of view |
| Color inconstancy | How far one material's color moves\
when the light or observer changes |
| Corresponding colors | Pairs of colors, under two lights, that\
look the same; the basis of CATs |
| D50, D65, A, C | Standard lights: D50 and D65 are daylight\
(printing and general use), A is tungsten,\
C is an older daylight standard |
| ΔE00 (CIEDE2000) | The standard color-difference formula,\
computed from CIELAB |
| ΔE(WLab) | The straight-line distance between two\
WLab values; a material color difference |
| Illuminant | A light, defined by how much power it\
gives at each wavelength |
| Least dissimilar match | Picking the sample under a new light that\
is made of the same material, even if it\
looks different |
| MAT\
(material adjustment transform) | Predicts a material's numbers under a\
different light, observer or both |
| Material color\
equivalency (MCE) | Treating colors as the same when they\
come from the same material |
| Metamerism | Two different spectra that match in one\
condition and not in another |
| Munsell notation | Hue, Value (lightness) and Chroma\
(colorfulness): 5R 5/6 is hue 5R,\
Value 5, Chroma 6 |
| Observer | The three sensitivity curves of a person,\
a standard observer or a camera |
| Observing condition | The observer and the light together |
| Practical Wpt | Wpt carried to a new condition through\
base reflectances you choose |
| Reference condition | The CIE 1931 observer under illuminant C,\
with the Munsell Renotation: the fixed\
basis of Wpt |
| Spectral reflectance | The fraction of light a material\
reflects at each wavelength |
| Wpt (Waypoint) | Material coordinates: W lightness,\
p red–green, t yellow–blue |
| Wpt normalization | The basic math steps, worked out for each\
observing condition, that turn an\
observer's three responses into Wpt |
| Wpt shift manifold | The cloud of Wpt points one material\
makes across many conditions |
| WLab (Waypoint-Lab) | Wpt reshaped so straight-line distance\
works as a color difference |

## Further reading

Read in this order: each one assumes the one before it.

1. **The idea of material color.** Logvinenko AD, Tokunaga R. Colour constancy as measured by least dissimilar matching. *Seeing and Perceiving* 2011;24:407–452. Also: An object-color space. *Journal of Vision* 2009;9:5.1–23.
2. **Wpt and MATs.** Derhak MW, Berns RS. [Introducing Wpt (Waypoint): a color equivalency representation for defining a material adjustment transform](https://doi.org/10.1002/col.21928). *Color Research & Application* 2015;40(6):535–549. Start with the introduction and the section on deriving the MAT.
3. **WLab.** Derhak MW, Berns RS. [Introducing WLab: going from Wpt (Waypoint) to a uniform material color equivalency space](https://doi.org/10.1002/col.21933). *Color Research & Application* 2015;40(6):550–563.
4. **Shift manifolds.** Derhak MW, Luo L, Berns RS. [Waypoint shift manifolds for object color evaluation and comparison](https://doi.org/10.1002/col.22477). *Color Research & Application* 2020.
5. **Metamerism and inconstancy metrics.** Derhak MW, Luo L, Berns RS. [Wpt (waypoint) shift manifold difference metrics for evaluation of varying observing-condition (observer + illuminant) metamerism and color inconstancy](https://doi.org/10.1002/col.22554). *Color Research & Application* 2020.
6. **The full treatment.** Derhak MW. *Spectrally Based Material Color Equivalency: Modeling and Manipulation.* PhD dissertation, Rochester Institute of Technology, 2015.
7. **Practical Wpt (in preparation).** Two papers on building Wpt from real-world reflectances, converting custom observers, and working from camera and display measurements alone.

Code and spreadsheets: the companion package described under "Getting started".
