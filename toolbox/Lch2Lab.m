function [ Lab ] = Lch2Lab( Lch )
%Lch2Lab converts vectors containing CIELCH values into vectors containing
%CIELAB values
%
%Argument:
%Lch - 3 by n matrix containing column vectors of CIELCH data
%
%Return:
%Lab - 3 by n matrix containing column vectors of CIELAB data
%
%Written January 2009 by Max Derhak

h = Lch(3,:) * pi / 180;

Lab = [Lch(1,:); ...
       cos(h).*Lch(2,:); ...
       sin(h).*Lch(2,:)];

end

