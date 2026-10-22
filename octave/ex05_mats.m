% ex05_mats - CATs and MATs: bridging observing conditions
%
% Guide section: "CATs and MATs: two ways to bridge conditions".
%  1. Measurements under illuminant A, carried to D65 (CIE 1931 observer) for
%     1,600 Munsell samples. A Wpt MAT is compared with two familiar CATs
%     (Bradford and CAT02, full adaptation) and with plain white scaling in XYZ.
%     The score is the mean DeltaE00 from the true D65 values: here the question
%     is what the material measures, which is a MAT's job, not a CAT's.
%  2. Converting the observer itself: the CIE 2015 2-degree observer's functions
%     carried to the CIE 1931 observer by a MAT (D65), scored on the same samples.
%  3. Two forms of one observer: LMS cone fundamentals to the same observer's
%     color-matching functions. The MAT recovers the exact relation.

addpath(fileparts(mfilename('fullpath'))); onrampSetup;
X = mun.X; o = cie.cmf2deg;

src = cie.illA; dst = cie.illD65;
xs = ref2XYZ(X, o, src); xd = ref2XYZ(X, o, dst);
ws = cmfillum2XYZ(o, src); wd = cmfillum2XYZ(o, dst);
labTrue = XYZ2Lab(xd, wd);
score = @(xyz) mean(deltaE00(XYZ2Lab(xyz, wd), labTrue));

As = getWptStruct(cie, o, src).xyz2wpt; Ad = getWptStruct(cie, o, dst).xyz2wpt;
mat = Ad \ As;                                  % into Wpt, then out to the destination
cat = @(S) S \ diag((S * wd) ./ (S * ws)) * S;  % von Kries scaling in the space S
bradford = [0.8951 0.2664 -0.1614; -0.7502 1.7135 0.0367; 0.0389 -0.0685 1.0296];
cat02 = [0.7328 0.4296 -0.1624; -0.7036 1.6975 0.0061; 0.0030 0.0136 0.9834];

printf('1. Illuminant A to D65, %d Munsell samples, mean DeltaE00 from the true D65 values\n', size(X, 2));
printf('   no adjustment (XYZ as measured)   %5.2f\n', score(xs));
printf('   white scaling in XYZ              %5.2f\n', score(cat(eye(3)) * xs));
printf('   Bradford CAT                      %5.2f\n', score(cat(bradford) * xs));
printf('   CAT02                             %5.2f\n', score(cat(cat02) * xs));
printf('   Wpt MAT                           %5.2f\n', score(mat * xs));

% 2. observer conversion: apply the MAT to the 2015 functions themselves
o15 = cie.cmf2deg2015;
M = getWptStruct(cie, o, dst).xyz2wpt \ getWptStruct(cie, o15, dst).xyz2wpt;
oConv = (M * o15')';
lab31 = XYZ2Lab(ref2XYZ(X, o, dst), cmfillum2XYZ(o, dst));
lab15 = XYZ2Lab(ref2XYZ(X, o15, dst), cmfillum2XYZ(o15, dst));
labCv = XYZ2Lab(ref2XYZ(X, oConv, dst), cmfillum2XYZ(oConv, dst));
printf('2. CIE 2015 2-degree observer to CIE 1931 under D65, mean DeltaE00 from true 1931 values\n');
printf('   2015 functions used as they are   %5.2f\n', mean(deltaE00(lab15, lab31)));
printf('   2015 functions converted by MAT   %5.2f\n', mean(deltaE00(labCv, lab31)));

% 3. same observer, two forms (CIE 170-2 relation between LMS and the 2015 XYZ functions)
Mlx = [1.94735469 -1.41445123 0.36476327; 0.68990272 0.34832189 0; 0 0 1.93485343];
lms = (Mlx \ o15')';
Mmat = getWptStruct(cie, o15, dst).xyz2wpt \ getWptStruct(cie, lms, dst).xyz2wpt;
xConv = ref2XYZ(X, (Mmat * lms')', dst); xTrue = ref2XYZ(X, o15, dst);
printf('3. LMS converted by MAT to the same observer''s XYZ functions: largest XYZ difference %.1e\n', max(abs(xConv(:) - xTrue(:))));
