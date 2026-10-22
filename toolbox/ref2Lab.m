function [Lab] = ref2Lab(ref, cmfObs, illum)
%ref2Lab converts reflectance data to Lab data reelative to illum
%  Lab = ref2Lab(ref, cmfObs, illum) 
%
%  Where:
%    ref - a reflectance column vector or a matrix where each column is
%          a reflectance vector
%    cmfObs - matrix containging color matching function for an observer
%    illum - power distribution for an illuminant
%
%  Written by Max Derhak (Feb 2009)

xyzIllum = cmfillum2XYZ(cmfObs, illum);
Lab = XYZ2Lab(ref2XYZ(ref, cmfObs, illum), xyzIllum);

end
