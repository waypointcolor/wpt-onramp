function [ wpt ] = WLab2Wpt( WLab )
%WLab2Wpt converts uniform WLab coordinates to Wpt coordinates based on
%hue adjusted deltaE94 chroma optimization
%
% Arguments:
%  -WLab is an array of WLab vectors
%
% Return:
%  -wpt is an array of Wpt vectors
%
% Written March 2014 by Max Derhak

%get polar notation
wch = Lab2Lch(WLab);

%undo hue based chroma logrithmic adjustment
h=wch(3,:);
sidx = (h>1 & h<181);
cidx = (h>104 & h<284);
r=zeros(1,length(h));
r(sidx) = sin((h(sidx)-1)*pi/180).^3;
r(cidx) = r(cidx)+0.39*cos((h(cidx)-14)*pi/180).^2;
d0 = 62*(r+0.31);
d1 = 0.36*(r+0.19);

wch(2,:) = 80*(exp(wch(2,:)./d0 + log(d1)) - d1);

    function W = DeLinearizeL(v)
        %Set up logical indexing arrays to apply cubic root
        W = (v + 16) / 116;
        vidx = W>6/29;
        notvidx = ~vidx;

        %calculate linear scalar factor
        three_d2 = 3 * (6/29)^2;

        %Apply cube to linear XYZ values using linear segment for darks
        W(vidx) = W(vidx).^3;
        W(notvidx) = (W(notvidx) - (4/29)) .* three_d2;
        W = 100*W;
    end

%Undo Lightness-chroma normalization
L5 = 51.576165618406904;
a = 0.026742553710937;
gv = 0.458886718750000;

tx=(wch(1,:)-L5);
s=exp(a*tx)/gv;
wch(2,:) = wch(2,:).*s;

%Undo linearization of Lightness
wch(1,:) = DeLinearizeL(wch(1,:));

%convert back to cartesian coords
wpt = Lch2Lab(wch);

end

