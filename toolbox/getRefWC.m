function [ wc ] = getRefWC( ref, wpts )

wpt = wpts.ref2wpt * ref;
wc = [wpt(1,:); sqrt(wpt(2,:).^2 + wpt(3,:).^2)];

end

