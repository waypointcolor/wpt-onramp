function [cie] = getCieStruct(lambda, getAll)

%getCieStruct Gets CIE observer and illuminant data
%  cie = getCieStruct(lambda, getALL) loads and intializes a structure with
%        CIE observer and illuminant data
%
%Arguments
% lambda = an optional vector argument that can provide specifies the
%  wavelengths to use for all data in the structure
%
%Return value
% cie = The structure members are as follows:
%
%  lambda:   vector containing wavelments for all data in structure
%  cmf2deg:  matrix containing XYZ sensitivities for 2 degree std observer
%            X = cmf2deg(:,1), Y = cmf2deg(:,2), Z = cmf2deg(:,3)
%  cmf10deg: matrix containing XYZ sensitivities for 10 degree std observer
%            X = cmf10deg(:,1), Y = cmf10deg(:,3), Z = cmf10deg(:,3)
%  illA:     vector containing CIE illuminant A power distribution
%  illC:     vector containing CIE illuminant C power distribution
%  illD65:   vector containing CIE illuminant D65 power distribution
%  illE:     vector containing CIE illuminant E power distribution
%  illF:     matrix containing vectors of CIE flourescent illuminant power
%            distributions
%  eigD:     eigenvector used to construct daylight illuminants
%
%  if getALL is defined then the following fields are also defined
%  rods:     vector containing CIE V' rod sensitivities
%  illD50:   vector containing CIE illuminant D50 power distribution
%  whiteLED: vector containing whiteLED power distribution
%  Written by Max Derhak (Sept 2008)

%a. load files
cmf2deg = load('CIE_2Deg_380-780-5nm.txt');
cmf10deg = load('CIE_10Deg_380-780-5nm.txt');
if exist('lambda')
    cmf2deg2015 = load('CIE_2Deg-2015_380-830-1nm.txt');
    cmf10deg2015 = load('CIE_10Deg-2015_380-830-1nm.txt');
    illA = load('CIE_IllA_300-830-5nm.txt');
    illC = load('CIE_IllC_300-830-5nm.txt');
    illD65 = load('CIE_IllD65_300-830-5nm.txt');
else
    cmf2deg2015 = load('CIE_2Deg-2015_380-780-5nm.txt');
    cmf10deg2015 = load('CIE_10Deg-2015_380-780-5nm.txt');
    illA = load('CIE_IllA_380-780-5nm.txt');
    illC = load('CIE_IllC_380-780-5nm.txt');
    illD65 = load('CIE_IllD65_380-780-5nm.txt');
end
illF = load('CIE_IllF_1-12_380-780-5nm.txt');

if exist('lambda') && (lambda(1)<380 || lambda(end)>780)
    eigD = load('CIE_eigD_300-830-10nm.txt');
else
    eigD = load('CIE_eigD_380-780-5nm.txt');
end

%b. create lambda members
cie.lambda = cmf2deg(:,1)';

[x y] = size(cie.lambda);

%strip wavelength data from each matrix as we put things in structure
cie.cmf2deg = cmf2deg(:,2:end);

cie.cmf10deg = cmf10deg(:,2:end);

cie.cmf2deg2015 = cmf2deg2015(:,2:end);

cie.cmf10deg2015 = cmf10deg2015(:,2:end);

cie.illA = illA(:,2:end);

cie.illC = illC(:,2:end);

cie.illD65 = illD65(:,2:end);

%c. synthetically create CIE illum E
cie.illE = ones(y, 1) * 100;

cie.illF = illF(:,2:end);

cie.eigD = eigD(:,2:end);


%If the lambda argment has wavelength information interplate everything to
%desired wavelengths
if exist('lambda')
    cie.cmf2deg = interp1(cie.lambda, cie.cmf2deg, lambda, 'linear', 'extrap');
    cie.cmf10deg = interp1(cie.lambda, cie.cmf10deg, lambda, 'linear', 'extrap');
    cie.cmf2deg2015 = interp1(cmf2deg2015(:,1), cie.cmf2deg2015, lambda, 'linear', 'extrap');
    cie.cmf10deg2015 = interp1(cmf10deg2015(:,1), cie.cmf10deg2015, lambda, 'linear', 'extrap');
    cie.illA = interp1(illA(:,1), cie.illA, lambda, 'linear', 'extrap')';
    cie.illC = interp1(illC(:,1), cie.illC, lambda, 'linear', 'extrap')';
    cie.illD65 = interp1(illD65(:,1), cie.illD65, lambda, 'linear', 'extrap')';
    cie.illE = interp1(cie.lambda, cie.illE, lambda, 'linear', 'extrap')';
    cie.illF = interp1(cie.lambda, cie.illF, lambda, 'linear', 'extrap');
    cie.eigD = interp1(eigD(:,1), cie.eigD, lambda, 'linear', 'extrap');
    
    %last but not least reset cie.lambda
    cie.lambda = lambda;
end

cie.prd = ones(length(cie.lambda), 1);

if exist('getAll')
    rods = load('CIE_Vprime_380-780-1nm.txt');
    cie.rods = interp1(rods(:,1), rods(:,2), cie.lambda, 'linear', 'extrap')';
    illWLED = load('WhiteLED.txt');
    cie.illWLED = interp1(illWLED(:,1), illWLED(:,2), cie.lambda)';
    cie.illWLED = cie.illWLED .* (100/cie.illWLED(find(cie.lambda==560)));
    cie.illWLED = cie.illWLED - min(cie.illWLED);
    
    cie.illD50 = cieIllD(5000, cie);
end
