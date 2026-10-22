function dE = deltaE00(Lab1, Lab2)
% deltaE00 CIEDE2000 colour difference with kL = kC = kH = 1.
%   dE = deltaE00(Lab1, Lab2), Lab1 and Lab2 being 3-by-n arrays of CIELAB
%   values (one colour per column).
%
% Implemented from the published formula, following the notes of Sharma, Wu
% and Dalal, "The CIEDE2000 color-difference formula: implementation notes,
% supplementary test data, and mathematical observations", Color Research and
% Application 30(1), 21-30, 2005, including their treatment of the hue
% difference and mean hue.

L1 = Lab1(1,:); a1 = Lab1(2,:); b1 = Lab1(3,:);
L2 = Lab2(1,:); a2 = Lab2(2,:); b2 = Lab2(3,:);

Cm = (sqrt(a1.^2 + b1.^2) + sqrt(a2.^2 + b2.^2)) / 2;
G = 0.5 * (1 - sqrt(Cm.^7 ./ (Cm.^7 + 25^7)));
ap1 = (1 + G) .* a1; ap2 = (1 + G) .* a2;
Cp1 = sqrt(ap1.^2 + b1.^2); Cp2 = sqrt(ap2.^2 + b2.^2);
hp1 = mod(atan2(b1, ap1) * 180 / pi, 360); hp1(Cp1 == 0) = 0;
hp2 = mod(atan2(b2, ap2) * 180 / pi, 360); hp2(Cp2 == 0) = 0;

dLp = L2 - L1;
dCp = Cp2 - Cp1;
dh = hp2 - hp1;
dh(dh > 180) = dh(dh > 180) - 360;
dh(dh < -180) = dh(dh < -180) + 360;
zeroC = (Cp1 .* Cp2) == 0;
dh(zeroC) = 0;
dHp = 2 * sqrt(Cp1 .* Cp2) .* sin(dh / 2 * pi / 180);

Lpm = (L1 + L2) / 2;
Cpm = (Cp1 + Cp2) / 2;
hs = hp1 + hp2;
hpm = hs / 2;
far = abs(hp1 - hp2) > 180;
hpm(far & hs < 360) = (hs(far & hs < 360) + 360) / 2;
hpm(far & hs >= 360) = (hs(far & hs >= 360) - 360) / 2;
hpm(zeroC) = hs(zeroC);

T = 1 - 0.17 * cos((hpm - 30) * pi / 180) + 0.24 * cos(2 * hpm * pi / 180) ...
      + 0.32 * cos((3 * hpm + 6) * pi / 180) - 0.20 * cos((4 * hpm - 63) * pi / 180);
dTheta = 30 * exp(-((hpm - 275) / 25).^2);
RC = 2 * sqrt(Cpm.^7 ./ (Cpm.^7 + 25^7));
SL = 1 + 0.015 * (Lpm - 50).^2 ./ sqrt(20 + (Lpm - 50).^2);
SC = 1 + 0.045 * Cpm;
SH = 1 + 0.015 * Cpm .* T;
RT = -sin(2 * dTheta * pi / 180) .* RC;

dE = sqrt((dLp ./ SL).^2 + (dCp ./ SC).^2 + (dHp ./ SH).^2 + RT .* (dCp ./ SC) .* (dHp ./ SH));
end
