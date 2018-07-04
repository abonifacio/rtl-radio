function [sos,g] = filtro()
Fs  = 2.048e6;                                 % Sampling Frequency (Hz)
Fn  = Fs/2;                                 % Nyquist Frequency
Fco =   250e3;                                 % Passband (Cutoff) Frequency
Fsb =   260e3;                                 % Stopband Frequency
Rp  =    1;                                 % Passband Ripple (dB)
Rs  =   10;                                 % Stopband Ripple (dB)
[n,Wn]  = buttord(Fco/Fn, Fsb/Fn, Rp, Rs);  % Filter Order & Wco
[b,a]   = butter(n,Wn);                     % Lowpass Is Default Design
[sos,g] = tf2sos(b,a);
end