function [XYZ] = ref2XYZ(ref, cmfObs, illum)

%ref2XYX converts reflectance data to XYZ tristimulus data
%  XYZ = ref2XYZ(ref, cmfObs, illum) 
%
%  Where:
%    ref - a reflectance column vector or a matrix where each column is
%          a reflectance vector
%    cmfObs - matrix containging color matching function for an observer
%    illum - power distribution for an illuminant
%
%  Written by Max Derhak (Sept 2008)

%first calculate normalization constant 
k = 100 / sum(diag(cmfObs(:,2))*illum);

%calculate XYZ tristimulus vector
XYZ = k .* cmfObs' * diag(illum) * ref; 
