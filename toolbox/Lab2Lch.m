function [ Lch ] = Lab2Lch( Lab )
%LAB2LCH converts vectors containing CIELAB values into vectors containing
%CIELCH values
%
%Argument:
%Lab - 3 by n matrix containing column vectors of CIELAB data
%
%Return:
%Lch - 3 by n matrix containing column vectors of CIELCH data
%
%Written January 2009 by Max Derhak

h = atan2(Lab(3,:), Lab(2,:))*180/pi;
idx = (h<0);
h(idx) = h(idx) + 360;

Lch = [Lab(1,:); ...
       sqrt(Lab(2,:).^2 + Lab(3,:).^2); ...
       h];

end

