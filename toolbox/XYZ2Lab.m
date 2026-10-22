function Lab = XYZ2Lab(XYZ, XYZn)
%This function converts tristimulus XYZ values to CIELAB values
%
%The arguments to this function are as follows:
%
% XYZ = a 3-by-n matrix of tristimulus values
% XYZn = a 3-b-1 vector of an illuminant white point (XYZn)
%
%Return value
% Lab = a 3-by-n matrix of CIELAB values

%normalize XYZ values by illuminant values in XYZn
if nargin<2
  XYZn=[96.42455651282464; 100.0; 82.46790940919662]; %default to D50
end

XYZ(1, :) = XYZ(1, :) ./ XYZn(1);
XYZ(2, :) = XYZ(2, :) ./ XYZn(2);
XYZ(3, :) = XYZ(3, :) ./ XYZn(3);

%Set up logical indexing arrays to apply cubic root
idx = XYZ>0.008856;
notidx = ~idx;

%Apply cubic root to normalized XYZ values using linear segment for darks
XYZ(idx) = XYZ(idx).^(1/3);
XYZ(notidx) = 7.787 * XYZ(notidx) + (16/116);

%store lab results from normalized values
Lab = [ 116*XYZ(2, :) - 16; ...
        500*(XYZ(1, :) - XYZ(2, :)); ...
        200*(XYZ(2, :) - XYZ(3, :))];

%end the function
end
