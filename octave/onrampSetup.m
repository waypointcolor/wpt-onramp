% onrampSetup - put the toolbox on the path and load what every example uses
%
% Defines, in the caller's workspace:
%   lambda  wavelengths, 380:5:780 nm
%   cie     CIE observers and illuminants (getCieStruct), plus cie.illD50
%   mun     the Munsell reflectances that carry the standard Wpt normalization
%
% Run it at the top of each example: onrampSetup

here = fileparts(mfilename('fullpath'));
addpath(fullfile(here, '..', 'toolbox'));
addpath(fullfile(here, '..', 'data'));
warning('off', 'all');

lambda = 380:5:780;
cie = getCieStruct(lambda);
cie.illD50 = cieIllD(5000, cie);
mun = load('munsell380_780_5_reconstC.mat');
