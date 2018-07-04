from subprocess import Popen, PIPE

demodulador = Popen(['python', 'fm-stdout.py'], stdout=PIPE)
fmedia = Popen(['python', 'log.py'],stdin=demodulador.stdout, stdout=PIPE)
# fmedia = Popen(['fmedia', '@stdin.wav', '--rate=44100','--channels=mono','--format=float32'],stdin=demodulador.stdout, stdout=PIPE)
# demodulador.stdout.close() # enable write error
out, err = fmedia.communicate()