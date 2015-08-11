%% to fit the curve in a Monte Carlo way
%% the 1 sigma error bar for one data point is given by the standard 
%% deviation of the photometric time series
%% for F125W it is 1.41%
%% for F160W it is 1.08%

function [pDistr, ampDistr]=MCFit(fn, stdPhot, nLoop, outputFn)
[t, ~, fB] = textread(fn, '%f %f %f');
pDistr = zeros(nLoop, 1);
ampDistr = zeros(nLoop, 1);
F = @(p,xdata)p(1)*sin((2*pi/p(2))*xdata+p(3)) + 1; % define the function
p0 = [0.01, 10.0, 0];
for i=1:nLoop 
    err = 1 + stdPhot * randn(size(fB));
    fB_1 = err .* fB;
    [pFit,~,~,~,~] = lsqcurvefit(F,p0,t,fB_1);
    pDistr(i) = pFit(2);
    ampDistr(i) = pFit(1);
end
csvwrite(outputFn, [pDistr, ampDistr])


    