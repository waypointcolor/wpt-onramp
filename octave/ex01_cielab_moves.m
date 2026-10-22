% ex01_cielab_moves - a material does not have one CIELAB value
%
% Guide sections: "What you already know: CIELAB and DeltaE" and
% "A material does not have one Lab value".
% The same three Munsell samples, and a spectrally flat gray, under three lights.
% CIELAB changes with the light, and by a different amount for each sample;
% only the gray stays put.

addpath(fileparts(mfilename('fullpath'))); onrampSetup;

base = readBase();
pick = {'5R 5/6', '5G 5/6', '5PB 5/6'};
R = [base.X(:, cellfun(@(n) find(strcmp(base.names, n)), pick)) 0.5 * ones(numel(lambda), 1)];
names = [pick {'50% gray'}];
ill = {cie.illD65, cie.illA, cie.illF(:, 11)}; iname = {'D65', 'A', 'F11'};

printf('CIELAB (L*, a*, b*), CIE 1931 observer\n%-10s', '');
printf('%26s', iname{:}); printf('%22s\n', 'DeltaE00 D65 to A');
for k = 1:numel(names)
  printf('%-10s', names{k});
  for i = 1:numel(ill), printf('   %6.1f %6.1f %6.1f   ', ref2Lab(R(:, k), cie.cmf2deg, ill{i})); end
  printf('%14.1f\n', deltaE00(ref2Lab(R(:, k), cie.cmf2deg, cie.illD65), ref2Lab(R(:, k), cie.cmf2deg, cie.illA)));
end
