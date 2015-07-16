function pFit=periodFit(fn, p0)
[t, ~, fB] = textread(fn, '%f %f %f');
figure();
F=@(p,xdata)p(1)*sin((2*pi/p(2))*xdata+p(3)) + 1;
[pFit,~,~,~,~] = lsqcurvefit(F,p0,t,fB);
t0 = linspace(min(t), max(t), 1000);
f0 = F(pFit, t0);
plot(t0, f0);
hold on; plot(t, fB, 'o');
xlabel('time');
ylabel('flux');

