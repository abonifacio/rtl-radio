from subprocess import Popen, PIPE

demodulador = Popen(['C:\\Users\\Augusto\\Dropbox\\fac\\Comunicaciones\\Comu2018_Lab1\\rtl-sdr-release\\x64\\rtl_sdr.exe', '-f','99.5e6','-'], stdout=PIPE)
fmedia = Popen(['python', 'log.py'],stdin=demodulador.stdout, stdout=PIPE)
# fmedia = Popen(['fmedia', '@stdin.wav', '--rate=44100','--channels=mono','--format=float32'],stdin=demodulador.stdout, stdout=PIPE)
# demodulador.stdout.close() # enable write error
out, err = fmedia.communicate()


# import serial

# ser = serial.Serial(
#     port='COM1',\
#     baudrate=9600,\
#     parity=serial.PARITY_NONE,\
#     stopbits=serial.STOPBITS_ONE,\
#     bytesize=serial.EIGHTBITS,\
#         timeout=0)

# print("connected to: " + ser.portstr)


# while True:
#     for c in ser.read():
#         print(c)

# ser.close()

