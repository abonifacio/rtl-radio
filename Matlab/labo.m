Fs = 2.048e6;
Fo = 91.1e6;
Bw1 = 200e3;
Bw2 = 15e3;

data = loadFile('Muestras-91.1');
%DEP(data,Fs,'Senial muestrada');
%FFT(data,Fs);

filtro180 = filtroscustom(Bw1,Fs);

data = filter(filtro180, data);
%DEP(data,Fs,'filtrada (180k)');

N1 = floor(Fs/(Bw1*2));
Fs = Fs/N1;
data = decimate(data,N1,'fir');
%DEP(data,Fs,'diezmada (1)');

W = 75e3;
D = 5;
kf = D*W;


xd = unwrap(angle(data));
xd = xd/(2*pi*kf); 
xd = [0, diff(xd)'.*Fs];
yd = xd-mean(xd); 
yd =  yd/max(abs(yd));

data = filter(filtroscustom(Bw2,Fs), yd);
%data = filter(filtro48k, yd);
%DEP(data,Fs,'filtrada (48k)');

%FFT(data,Fs);
N2 = floor(Fs/(Bw2*2));
Fs = Fs/N2;
disp(N2);
disp(Fs);
data = decimate(data,N2,'fir');
%DEP(data,Fs,'diezmada (2)');

%FFT(data,Fs);


Z_out = data ./ max(abs(data));
sound(Z_out,Fs);

%senial = discriminar(senial);
%DEP(data,Fs,'discriminada');

%senial = low_pass(senial,F_bw2);
%DEP(data,Fs,'filtrada (20k)');

%senial = decimate(senial,F_bw2)



%[f,Sxx] = DEP(data,2.048e6,'espectro FM');

%F = fft(data,2097152);
%F = fftshift(F);

%plot(f,F);

% filtro = filtro250k;

% x1 = filter(filtro, data);

% DEP(x1,2.048e6,'espectro FM');

% N1 = 1024e6 / 250e3;

% x_N1 = decimate(x1,N1,'fir');


% DEP(x1_N1,2*N1,'espectro FM');



