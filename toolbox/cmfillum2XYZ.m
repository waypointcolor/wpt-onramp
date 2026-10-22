function [ XYZ ] = cmfillum2XYZ( cmf, illum)
%cmfillum2XYZ(cmf, illum) calculates the XYZ coordinates for the given 
% obsever and illumnant
%
%Written Jan 2009 - by Max Derhak

XYZ = ref2XYZ(ones(length(illum),1), cmf, illum);

end

