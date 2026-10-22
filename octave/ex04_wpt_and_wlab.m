% ex04_wpt_and_wlab - from a spectrum to Wpt and WLab, with sanity checks
%
% Guide sections: "Wpt", "WLab" and "Getting started".
%  1. Recipe: reflectance -> XYZ -> Wpt -> WLab, for one sample under three lights.
%  2. A spectrally flat 50% gray is WLab (76.1, 0, 0) under every light.
%  3. WLab converts back to Wpt exactly.
%  4. The form of the observer does not matter: the CIE 2015 2-degree observer
%     given as cone fundamentals (LMS) or as color-matching functions gives the
%     same Wpt.

addpath(fileparts(mfilename('fullpath'))); onrampSetup;
base = readBase();
r = base.X(:, strcmp(base.names, '5PB 5/6'));

ill = {cie.illD65, cie.illA, cie.illF(:, 11)}; iname = {'D65', 'A', 'F11'};
printf('1. Munsell 5PB 5/6, CIE 1931 observer\n');
for i = 1:3
  w = getWptStruct(cie, cie.cmf2deg, ill{i});
  xyz = ref2XYZ(r, cie.cmf2deg, ill{i});
  wpt = w.xyz2wpt * xyz;          % the same as w.ref2wpt * r
  printf('   %-4s XYZ %6.2f %6.2f %6.2f  Wpt %6.2f %6.2f %6.2f  WLab %6.2f %6.2f %6.2f\n', iname{i}, xyz, wpt, Wpt2WLab(wpt));
end

printf('2. 50%% gray, CIE 1931 observer\n');
for i = 1:3
  w = getWptStruct(cie, cie.cmf2deg, ill{i});
  printf('   %-4s WLab %6.2f %6.2f %6.2f\n', iname{i}, Wpt2WLab(w.ref2wpt * (0.5 * ones(numel(lambda), 1))));
end

w = getWptStruct(cie, cie.cmf2deg, cie.illD65);
wpt = w.ref2wpt * mun.X;
printf('3. WLab back to Wpt, %d Munsell samples: largest error %.1e\n', size(mun.X, 2), max(max(abs(WLab2Wpt(Wpt2WLab(wpt)) - wpt))));

% CIE 170-2 relation between the 2015 2-degree XYZ functions and LMS cone fundamentals
M = [1.94735469 -1.41445123 0.36476327; 0.68990272 0.34832189 0; 0 0 1.93485343];
lms = (M \ cie.cmf2deg2015')';
wx = getWptStruct(cie, cie.cmf2deg2015, cie.illD65);
wl = getWptStruct(cie, lms, cie.illD65);
d = abs(wx.ref2wpt * mun.X - wl.ref2wpt * mun.X);
printf('4. CIE 2015 observer as XYZ functions or as LMS: largest Wpt difference %.1e\n', max(d(:)));
