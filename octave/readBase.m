function base = readBase()
% readBase - the 40 Munsell reflectances (Value 5, Chroma 6) that set up Wpt
%   base.names  1x40 cell of Munsell notations
%   base.X      81x40 reflectances, 380:5:780 nm
here = fileparts(mfilename('fullpath'));
f = fullfile(here, '..', 'toolbox', 'wpt_base_munsell40.csv');
fid = fopen(f); hdr = fgetl(fid); fclose(fid);
h = strsplit(hdr, ',');
base.names = h(2:end);
d = dlmread(f, ',', 1, 0);
base.X = d(:, 2:end);
end
