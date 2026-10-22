% ex02_purplish_blue - the worked example: a ColorChecker patch and its metameric twin
%
% Guide sections: "A material does not have one Lab value" and
% "WLab: measuring difference between materials" (the example, revisited).
% Needs data/ColorChecker_380-780-5nm.txt and data/MetaChecker_380-780-5nm.txt
% (see DATA.md). Writes results/purplish_blue_spectra.csv for the chart.

addpath(fileparts(mfilename('fullpath'))); onrampSetup;
need = {'ColorChecker_380-780-5nm.txt', 'MetaChecker_380-780-5nm.txt'};
for k = 1:2
  if ~exist(need{k}, 'file'), error('ex02: put %s in data/ (see DATA.md)', need{k}); end
end
c = load(need{1}); c = c(:, 2:end);
m = load(need{2}); m = m(:, 2:end);
k = 8;   % Purplish Blue

o = cie.cmf2deg;
wD = getWptStruct(cie, o, cie.illD65); wA = getWptStruct(cie, o, cie.illA);
labD = @(r) ref2Lab(r, o, cie.illD65); labA = @(r) ref2Lab(r, o, cie.illA);
wlD = @(r) Wpt2WLab(wD.ref2wpt * r); wlA = @(r) Wpt2WLab(wA.ref2wpt * r);
dist = @(a, b) sqrt(sum((a - b).^2));

printf('Purplish Blue, CIE 1931 observer          real patch              twin\n');
printf('CIELAB under D65            %6.1f %6.1f %6.1f    %6.1f %6.1f %6.1f\n', labD(c(:, k)), labD(m(:, k)));
printf('CIELAB under A              %6.1f %6.1f %6.1f    %6.1f %6.1f %6.1f\n', labA(c(:, k)), labA(m(:, k)));
printf('CIELAB change, DeltaE00     %20.1f %23.1f\n', deltaE00(labD(c(:, k)), labA(c(:, k))), deltaE00(labD(m(:, k)), labA(m(:, k))));
printf('WLab under D65              %6.1f %6.1f %6.1f    %6.1f %6.1f %6.1f\n', wlD(c(:, k)), wlD(m(:, k)));
printf('WLab under A                %6.1f %6.1f %6.1f    %6.1f %6.1f %6.1f\n', wlA(c(:, k)), wlA(m(:, k)));
printf('WLab change, DeltaE(WLab)   %20.1f %23.1f\n', dist(wlD(c(:, k)), wlA(c(:, k))), dist(wlD(m(:, k)), wlA(m(:, k))));
printf('Under A the two are DeltaE00 %.1f apart\n', deltaE00(labA(c(:, k)), labA(m(:, k))));

% the familiar alternative: carry the A values to D65 with a CAT (CAT02, full adaptation) before comparing
cat02 = [0.7328 0.4296 -0.1624; -0.7036 1.6975 0.0061; 0.0030 0.0136 0.9834];
wD65 = cmfillum2XYZ(o, cie.illD65); wIllA = cmfillum2XYZ(o, cie.illA);
Mcat = cat02 \ diag((cat02 * wD65) ./ (cat02 * wIllA)) * cat02;
labCat = @(r) XYZ2Lab(Mcat * ref2XYZ(r, o, cie.illA), wD65);
printf('CIELAB with CAT02, change   %20.1f %23.1f\n', deltaE00(labD(c(:, k)), labCat(c(:, k))), deltaE00(labD(m(:, k)), labCat(m(:, k))));

% the 18 chromatic patches: which one moves more, the real patch or its twin?
dLc = deltaE00(labD(c(:, 1:18)), labA(c(:, 1:18))); dLm = deltaE00(labD(m(:, 1:18)), labA(m(:, 1:18)));
dWc = dist(wlD(c(:, 1:18)), wlA(c(:, 1:18)));      dWm = dist(wlD(m(:, 1:18)), wlA(m(:, 1:18)));
dKc = deltaE00(labD(c(:, 1:18)), labCat(c(:, 1:18))); dKm = deltaE00(labD(m(:, 1:18)), labCat(m(:, 1:18)));
printf('Of 18 chromatic patches, the real patch moves more than its twin: CIELAB %d, CIELAB with CAT02 %d, WLab %d\n', ...
       sum(dLc > dLm), sum(dKc > dKm), sum(dWc > dWm));

% spectra for the chart, 380-730 nm
v = find(lambda <= 730);
out = fullfile(fileparts(mfilename('fullpath')), '..', 'results', 'purplish_blue_spectra.csv');
f = fopen(out, 'w'); fprintf(f, 'nm,real,twin,D65_rel560,A_rel560\n');
d = cie.illD65 / cie.illD65(lambda == 560) * 100; a = cie.illA / cie.illA(lambda == 560) * 100;
fprintf(f, '%d,%.4f,%.4f,%.2f,%.2f\n', [lambda(v); c(v, k)'; m(v, k)'; d(v)'; a(v)']);
fclose(f);
