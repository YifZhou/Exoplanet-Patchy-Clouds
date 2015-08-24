function pDistr=MCFit_fixP(fn1, fn2, err1, err2, nLoop, outputFN)
M1 = csvread(fn1, 1);
t1 = M1(:, 1);
fB1 = M1(:, 2);

M2 = csvread(fn2, 1);
t2 = M2(:, 1);
fB2 = M2(:, 2);

pDistr = zeros(nLoop, 1);
amp125 = zeros(nLoop, 1);
amp160 = zeros(nLoop, 1);
phase125 = zeros(nLoop, 1);
phase160 = zeros(nLoop, 1);
p0 = [0.01 10.0, 0, 0.01, 0];
for i=1:nLoop
    err1_1 = err1 .* randn(size(fB1));
    fB1_1 = fB1 + err1_1;
    err2_1 = err2 .* randn(size(fB2));
    fB2_1 = fB2 + err2_1;
    F=@(p)[(p(1)*sin((2*pi/p(2))*t1+p(3)) + 1 - fB1_1)./err1; ...
           (p(4)*sin((2*pi/p(2))*t2+p(5)) + 1 - fB2_1)./err2];
    [p, ~] = lsqnonlin(F,p0);
    pDistr(i) = p(2);
    amp125(i) = p(1);
    amp160(i) = p(4);
    phase125(i) = p(3);
    phase160(i) = p(5);
end
csvwrite(outputFN, [pDistr, amp125, phase125, amp160, phase160]);
