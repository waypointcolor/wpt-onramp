% ex06_inconstancy_metamerism - what WLab distances tell you
%
% Guide section: "What you can do with it".
% A Munsell sample (5PB 5/6) and a metameric twin made for this example: the
% twin adds a "metameric black" to the sample's reflectance, a wavy spectrum
% that the CIE 1931 observer cannot see under D65, so the two match exactly there.
% Then, all in WLab:
%   color inconstancy - how far each material moves from itself when the light changes
%   metamerism        - how far apart the two drift under other lights
%   observer metamerism - how far apart they are for the CIE 1964 observer
% Writes results/metamer_example.csv (wavelength, sample, twin).

addpath(fileparts(mfilename('fullpath'))); onrampSetup;
base = readBase();
r1 = base.X(:, strcmp(base.names, '5PB 5/6'));

% build the twin: add a wavy component, then keep it a physical reflectance (0..1)
% while holding its CIE 1931 / D65 tristimulus values equal to the original's
K = cie.cmf2deg' * diag(cie.illD65);
wave = 0.25 * sin(2 * pi * (lambda' - 380) / 90);
r2 = r1 + wave;
for it = 1:200
  r2 = min(max(r2, 0), 1);
  r2 = r2 - pinv(K) * (K * r2 - K * r1);
end

cond = {cie.cmf2deg, cie.illD65, 'CIE 1931, D65'; cie.cmf2deg, cie.illA, 'CIE 1931, A'; ...
        cie.cmf2deg, cie.illF(:, 11), 'CIE 1931, F11'; cie.cmf10deg, cie.illD65, 'CIE 1964, D65'};
wl = zeros(3, 2, rows(cond));
for c = 1:rows(cond)
  w = getWptStruct(cie, cond{c, 1}, cond{c, 2});
  wl(:, :, c) = Wpt2WLab(w.ref2wpt * [r1 r2]);
end
dist = @(a, b) sqrt(sum((a - b).^2));

printf('5PB 5/6 and its twin, DeltaE(WLab)\n');
printf('%-16s %12s %22s %22s\n', 'condition', 'between them', 'sample moved (D65)', 'twin moved (D65)');
for c = 1:rows(cond)
  printf('%-16s %12.2f %22.2f %22.2f\n', cond{c, 3}, dist(wl(:, 1, c), wl(:, 2, c)), ...
         dist(wl(:, 1, c), wl(:, 1, 1)), dist(wl(:, 2, c), wl(:, 2, 1)));
end
printf('Twin stays within 0..1: %d; largest XYZ difference under 1931/D65: %.1e\n', all(r2 >= 0 & r2 <= 1), max(abs(K * (r2 - r1))));

out = fullfile(fileparts(mfilename('fullpath')), '..', 'results', 'metamer_example.csv');
f = fopen(out, 'w'); fprintf(f, 'nm,sample_5PB_5_6,twin\n');
fprintf(f, '%d,%.4f,%.4f\n', [lambda; r1'; r2']);
fclose(f);
