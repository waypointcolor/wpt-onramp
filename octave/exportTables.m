% exportTables - write the tables that the Python module and the spreadsheets read
%
% Writes, into toolbox/ and excel/:
%   toolbox/spectral_tables_380_780_5.csv  CIE observers and illuminants at 5 nm
%   toolbox/wpt_base_munsell40.csv          the 40 Munsell reflectances (Value 5, Chroma 6)
%   toolbox/wpt_reference_pt.csv            their reference p and t (CIE 1931, illuminant C)
%   excel/wpt_matrices.csv                  XYZ-to-Wpt and Wpt-to-XYZ for common conditions
%
% The Python module and the spreadsheets are checked against these files, so rerun
% this script whenever the toolbox changes.

addpath(fileparts(mfilename('fullpath'))); onrampSetup;
here = fileparts(mfilename('fullpath'));
tb = fullfile(here, '..', 'toolbox');

% CIE tables
cols = {'cie1931_x','cie1931_y','cie1931_z','cie1964_x','cie1964_y','cie1964_z', ...
        'cie2015_2_x','cie2015_2_y','cie2015_2_z','illA','illC','illD50','illD65','illE','illF2','illF11'};
T = [lambda' cie.cmf2deg cie.cmf10deg cie.cmf2deg2015 cie.illA cie.illC cie.illD50 cie.illD65 cie.illE cie.illF(:,2) cie.illF(:,11)];
f = fopen(fullfile(tb, 'spectral_tables_380_780_5.csv'), 'w');
fprintf(f, 'nm,%s\n', strjoin(cols, ','));
fprintf(f, [repmat('%.10g,', 1, size(T, 2) - 1) '%.10g\n'], T');
fclose(f);

% The 40 base reflectances and their reference p, t (taken from getWptStruct.m itself)
s = [14 41 71 99 136 171 202 239 271 302 345 373 402 429 467 501 532 569 600 631 675 703 731 758 798 829 862 901 933 965 1008 1038 1066 1093 1132 1163 1198 1233 1265 1298];
txt = fileread(fullfile(tb, 'getWptStruct.m'));
i = strfind(txt, 'mpt = [['); j = strfind(txt, ']]'''); eval([txt(i(1):j(1) + 2) ';']);
fam = {'R','YR','Y','GY','G','BG','B','PB','P','RP'};
names = cell(1, 40);
for k = 1:40
  H = mun.HVC(s(k), 1); hf = floor(H); st = (H - hf) * 10;
  if st < 1e-9, st = 10; hf = hf - 1; end
  names{k} = sprintf('%g%s 5/6', st, fam{mod(hf, 10) + 1});
end
f = fopen(fullfile(tb, 'wpt_base_munsell40.csv'), 'w');
fprintf(f, 'nm,%s\n', strjoin(names, ','));
fprintf(f, [repmat('%.10g,', 1, 40) '%.10g\n'], [lambda' mun.X(:, s)]');
fclose(f);
f = fopen(fullfile(tb, 'wpt_reference_pt.csv'), 'w');
fprintf(f, 'sample,p,t\n');
for k = 1:40, fprintf(f, '%s,%.15g,%.15g\n', names{k}, mpt(1, k), mpt(2, k)); end
fclose(f);

% The 1,600 Munsell reflectances, for the examples that use many materials
f = fopen(fullfile(tb, 'munsell1600_380_780_5.csv'), 'w');
fprintf(f, 'nm%s\n', sprintf(',m%d', 1:size(mun.X, 2)));
fprintf(f, [repmat('%.9g,', 1, size(mun.X, 2)) '%.9g\n'], [lambda' mun.X]');
fclose(f);

% Check values for the other languages: Wpt and WLab of the 1,600 samples, CIE 1931 / D65
w = getWptStruct(cie, cie.cmf2deg, cie.illD65);
wpt = w.ref2wpt * mun.X;
f = fopen(fullfile(here, '..', 'results', 'check_1931_D65.csv'), 'w');
fprintf(f, 'W,p,t,Lw,aw,bw\n');
fprintf(f, '%.10g,%.10g,%.10g,%.10g,%.10g,%.10g\n', [wpt; Wpt2WLab(wpt)]);
fclose(f);

% Wpt matrices for common observing conditions
obs = {cie.cmf2deg, cie.cmf10deg}; on = {'CIE 1931 2deg', 'CIE 1964 10deg'};
ill = {cie.illC, cie.illD50, cie.illD65, cie.illA, cie.illE, cie.illF(:,2), cie.illF(:,11)};
iname = {'C', 'D50', 'D65', 'A', 'E', 'F2', 'F11'};
f = fopen(fullfile(here, '..', 'excel', 'wpt_matrices.csv'), 'w');
fprintf(f, 'condition,observer,illuminant,Xn,Yn,Zn');
fprintf(f, ',%s', 'A11','A12','A13','A21','A22','A23','A31','A32','A33','B11','B12','B13','B21','B22','B23','B31','B32','B33');
fprintf(f, '\n');
for o = 1:2
  for k = 1:numel(ill)
    w = getWptStruct(cie, obs{o}, ill{k});
    wn = cmfillum2XYZ(obs{o}, ill{k});
    A = w.xyz2wpt; B = inv(A);
    fprintf(f, '%s %s,%s,%s,%.10g,%.10g,%.10g', on{o}, iname{k}, on{o}, iname{k}, wn);
    fprintf(f, ',%.12g', A'(:)); fprintf(f, ',%.12g', B'(:)); fprintf(f, '\n');
  end
end
fclose(f);
printf('exportTables: wrote spectral tables, base set, reference p,t and %d matrices\n', 2 * numel(ill));
