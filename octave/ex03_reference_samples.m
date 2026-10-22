% ex03_reference_samples - the 42 samples that set up Wpt, in Wpt
%
% Guide section: "Wpt: coordinates for the material".
% White, the 40 Munsell colors at Value 5 / Chroma 6 and the vivid yellow
% (3.75Y 8/14), in Wpt under the reference condition (CIE 1931, illuminant C).
% White lands on the W axis at 100; the 40 colors share one W and sit near one
% circle; the yellow points along +t at 100. Writes results/reference_samples.csv
% with approximate sRGB colors (D65) for the swatch picture.

addpath(fileparts(mfilename('fullpath'))); onrampSetup;
base = readBase();
yellow = mun.X(:, 1572);   % Munsell 3.75Y 8/14 in the toolbox set
R = [ones(numel(lambda), 1) base.X yellow];
names = [{'N10 (white)'} base.names {'3.75Y 8/14'}];

w = getWptStruct(cie, cie.cmf2deg, cie.illC);
wpt = w.ref2wpt * R;

xyz = ref2XYZ(R, cie.cmf2deg, cie.illD65) / 100;
M = [3.2406 -1.5372 -0.4986; -0.9689 1.8758 0.0415; 0.0557 -0.2040 1.0570];
g = min(max(M * xyz, 0), 1); k = g <= 0.0031308; g(k) = 12.92 * g(k); g(~k) = 1.055 * g(~k).^(1 / 2.4) - 0.055;

printf('%-12s %7s %7s %7s %7s\n', 'sample', 'W', 'p', 't', 'chroma');
for i = 1:numel(names)
  printf('%-12s %7.2f %7.2f %7.2f %7.2f\n', names{i}, wpt(:, i), hypot(wpt(2, i), wpt(3, i)));
end
ch = hypot(wpt(2, 2:41), wpt(3, 2:41));
printf('40 colors: W %.2f to %.2f; chroma mean %.2f, range %.2f to %.2f\n', min(wpt(1, 2:41)), max(wpt(1, 2:41)), mean(ch), min(ch), max(ch));

out = fullfile(fileparts(mfilename('fullpath')), '..', 'results', 'reference_samples.csv');
f = fopen(out, 'w'); fprintf(f, 'sample,W,p,t,srgb\n');
for i = 1:numel(names), fprintf(f, '%s,%.4f,%.4f,%.4f,#%02x%02x%02x\n', names{i}, wpt(:, i), round(255 * g(:, i))); end
fclose(f);
