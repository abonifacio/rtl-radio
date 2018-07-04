function [f, Sxx] = DEP(x,fs,signal_name)
% [f, Sxx] = DEP(x,fs,signal_name)
% INPUTS:
%    x  = se~nal de entrada
%    fs = frecuencia de muestreo
%    signal_name = cadena de caracteres para el titulo. Ej. 'Se~nal antena'
% OUTPUTS:
%   f = vector de frecuencias donde se evalu ?o la DEP
%   Sxx = Estimacion de la DEP
[Sxx,f] = pwelch(x,ones(1,2.048e6),0,[],fs,'twosided');
Sxx = fftshift(Sxx); f = fftshift(f);
f(1:floor(length(f)/2)) = f(1:floor(length(f)/2)) - fs;
figure('units','normalized','outerposition',[0 0 1 1]);
plot(f,Sxx); xlim([-fs/2 fs/2]);
set(gca, 'FontSize', 18);
legend('S_{XX}(f)','Location','NorthEast');grid on;
xlabel('f [Hz]','Interpreter','Latex','FontSize',20);
title(['DEP de ' signal_name],'FontSize',20);
grid on;
end