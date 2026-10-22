function [ WLab ] = Wpt2WLab( wpt )
%Wpt2WLab converts wpt coordinates to WLab coordinates based on
%hue adjusted deltaE94 chroma optimization
%
% Arguments:
%  -wpt is an array of wpt vectors
%
% Return:
%  -WLab is an array of WLab vectors
%
% Written March 2014 by Max Derhak

%get polar notation
wch = Lab2Lch(wpt);

    function lw = LinearizeW(w)
        %Set up logical indexing arrays to apply cubic root
        Y=w/100;
        vidx = Y>(6/29)^3;
        notvidx = ~vidx;

        %Apply cubic root to normalized Y values using linear segment for darks
        Y(vidx) = Y(vidx).^(1/3);
        Y(notvidx) = ((1/3)*(29/6)^2) * Y(notvidx) + (16/116);

        lw = 116*Y - 16;
    end

wch(1,:) = LinearizeW(wch(1,:));

L5 = 51.576165618406904;
a = 0.026742553710937;
gv = 0.458886718750000;

%make chroma consistant with Lightness
tx=(wch(1,:)-L5);
s=exp(a*tx)/gv;
wch(2,:) = wch(2,:)./s;

%adjust chroma based on hue to match DeltaE94 chroma scale
h=wch(3,:);
sidx = (h>1 & h<181);
cidx = (h>104 & h<284);
r=zeros(1,length(h));
r(sidx) = sin((h(sidx)-1)*pi/180).^3;
r(cidx) = r(cidx)+0.39*cos((h(cidx)-14)*pi/180).^2;
b1 = 62*(r+0.31);
b2 = 0.36*(r+0.19);

wch(2,:) = b1.*(log(wch(2,:)/80+b2)-log(b2));

%convert back to cartesian coords
WLab = Lch2Lab(wch);

end

