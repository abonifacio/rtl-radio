function [f, Y] = FFT(data,fs)
L=length(data); 
NFFT=2^nextpow2(L); 
Y=fft(data,NFFT)/L; 
f=fs/2*linspace(0,1,NFFT/2+1);
figure(3)
plot(f,2*abs(Y(1:NFFT/2+1)))
end