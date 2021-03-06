%% to fit the curve in a Monte Carlo way
%% the 1 sigma error bar for one data point is given by the standard 
%% deviation of the photometric time series
%% for F125W it is 1.34%
%% for F160W it is 1.12%

function [pDistr, ampDistr, phaseDistr]=MCFit(fn, err, nLoop, outputFn)
M = csvread(fn, 1);
t = M(:, 1);
fB = M(:, 2);
%err = M(:, 3);
pDistr = zeros(nLoop, 1);
ampDistr = zeros(nLoop, 1);
phaseDistr = zeros(nLoop, 1);
F = @(p,xdata)p(1)*sin((2*pi/p(2))*xdata+p(3)) + 1; % define the function
p0 = [0.01, 10.0, 0];
for i=1:nLoop 
    err_1 = err * randn(size(fB));
    fB_1 = fB + err_1;
    [pFit,~,~,~,~] = lsqcurvefit(F,p0,t,fB_1);
    pDistr(i) = pFit(2);
    ampDistr(i) = pFit(1);
    phaseDistr(i) = pFit(3);
end
csvwrite(outputFn, [pDistr, ampDistr, phaseDistr])
