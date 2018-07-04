function [ Hd ] = filtroscustom( Freq,  Fs )
 d = fdesign.lowpass('Fp,Fst,Ap,Ast',Freq,Freq*1.1,0.5,40,Fs);
 Hd = design(d,'equiripple');
end

