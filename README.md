# Informe de SDR

El proyecto tiene dos carpetas, Matlab y Python. Dentro de Python se encuentra lo último desarrollado, los scripts de Matlab fueron pruebas iniciales para ver si era correcta la solución del problema antes de indagar sobre procesamiento con Python. Lo terminé realizando en Python porque me pareció mas interesante que Matlab, más que nada porque está más cerca de ser una aplicación real y no un script.

El demodulado en sí no fué lo que demoró la entrega sino el hecho de que quería entregar la solución en tiempo real, pero fallé de todas la formas que se me ocurrieron. De todas formas entrego un script de demodulación finita y otro que tiene el mejor intento de lo que sería una demodulación en tiempo real


## Instalación
Utilicé la version de Python **3.6.5**. Todas las librerías están listadas en el archivo `requirements.txt` y son instalables mediante `pip`.

	Nota: Fui probando varias librerías a lo largo del desarrollo, por lo que es posible que me haya olvidado de anotar alguna, de todas formas siempre fueron instaladas mediante pip 

## Simple

### fm-single.py 

Para la lectura de muestras se encontró una librería en Python que funciona como un wrapper de rtl en C, [pyrtlsdr](https://github.com/roger-/pyrtlsdr). 

Al crear una instancia del `RtlSdr` se busca el Dongle que esté conectado. Se le pide N muestras a una dada frecuencia central y este responde ya con el `numpy` complejo, es decir, realiza la conversión de los bytes `i` e `i+1`.


Este archivo ejecutable por consola mediante

```sh
C:\comunicaciones\Python>python fm-single.py -h

usage: fm-single.py [-h] [-n N] [-f FO] [--plot]

Procesar N muestras de FM.

optional arguments:
  -h, --help  show this help message and exit
  -n N        numero de muestras ej:1024e4
  -f FO       frecuencia centro en MHz ej:91.3
  --plot      Mostrar graficos de DEP y FFT

```

Parametros
- **n**: por defecto es 1024e4. No funciona bien con cualquier número por cuestiones de la libería 
- **f**: por defecto es 91.3 
- **--plot**: flag que activa los gráficos una vez terminado de reproducir e sonido 

Por ejemplo:

```sh
C:\comunicaciones\Python>python fm-single.py -f 92.1
Found Fitipower FC0012 tuner
0.8214776515960693 - inicio toma de muestras
8.903372764587402 - fin toma de muestras
8.903372764587402 - primer filtro
9.515150785446167 - primer diezmado
11.672977924346924 - discriminado
11.90323805809021 - segundo filtro
11.922728538513184 - segundo diezmado
11.984881162643433 - normalizado
11.990418672561646 - reproduciendo audio
17.31265091896057 - fin reproduccion
```


El programa empieza a tomar el tiempo cuando se inicia y los tiempos que se imprimen son los segundos que pasaron desde ese inicio.
Como se puede ver, la toma de muestras dura aproximadamente **8** segundos y el audio se reproduce en **5**. Si bien esta puede no ser la forma adecueada de leer muestras en tiempo real, la diferencia de tiempos es bastante y no la pude reducir.

### plotter.py

Esta clase permite ir agregando gráficos de manera dínamica para que mostrarlos al final de la ejecución agrupados en dos figuras 

```python
class Plotter:

	def __init__(self,Fs,Fo):
		self.subplotDEP = 0
		self.subplotFFT = 0
		self.Fs = Fs
		self.Fo = Fo

	def clear(self):
		self.subplotDEP = 0
		self.subplotFFT = 0
		plt.figure(1)
		plt.clf()
		plt.figure(2)
		plt.clf()

	def plotBoth(self,senial,nombre):
		self.DEP(senial,nombre)
		self.FFT(senial,nombre)

	def DEP(self,senial,nombre):
		self.subplotDEP+=1
		plt.figure(1)
		plt.subplot(320 + self.subplotDEP)
		plt.title("DEP de senial "+nombre)
		plt.psd(senial, NFFT=4096, Fs=self.Fs,Fc=self.Fo,sides='twosided')

	def FFT(self,senial,nombre):
		self.subplotFFT+=1
		NFFT = len(senial)
		f = np.multiply(self.Fs/2,np.linspace(0, 1,int(NFFT/2)+1))
		Y = np.fft.fft(senial,NFFT)/NFFT
		plt.figure(2)
		plt.subplot(320 + self.subplotFFT)
		plt.title("FFT de senial "+nombre)
		plt.semilogy(f, np.multiply(2,np.abs(Y[0:int(NFFT/2)+1])))
		plt.xlabel('f [kHz]')
		plt.grid()

	def show(self):
		plt.show()
```

### temporizador.py

Módulo usado para armar una línea de tiempo del programa.

```` python
class Temporizador:

	base_time = time.time()
	timestamps = []

	def tag(self,tag):
		self.timestamps.append({'tag':tag,'timestamp':(time.time()-self.base_time)})

	def to_string(self):
		st = ''
		for inst in self.timestamps:
			st+=str(inst['timestamp'])+' - '+inst['tag']+'\n'
		return st

	def print(self):
		print(self.to_string())

````


## Tiempo Real 

### fm-realtime.py

Para la demodulación en tiempo real primero se tiene que correr el programa `rtl_tcp` mediante consola especificando la frecuencia deseada a demodular.

```sh
C:\rtl-sdr-release\x64> rtl_tcp -f 92.1e6
```

En otra consola ejecutar

```sh
C:\comunicaciones\Python>python fm-realtime.py
```

Probé varias cosas, entre ellas crear más de un Thread `consumer` para paralelizar el procesamiento de la señal pero el problema creo que radica en la toma de muestras más que nada. 

Además, la librería [pyrtlsdr](https://github.com/roger-/pyrtlsdr), provee dos formas de obtener muestras en tiempo real que el creador define como experimentales.

La siguiente abre un stream de muestras para que puedan ser procesadas continuamente

```python
async def streaming():
    sdr = RtlSdr()

    async for samples in sdr.stream():
        # do something with samples
        # ...

loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())
``` 

Y la siguiente mediante es un wrapper de la función de TPC que ya provee `rtlsdr_release`

```python
server = RtlSdrTcpServer(hostname='192.168.1.100', port=12345)
server.run_forever()
# Will listen for clients until Ctrl-C is pressed

# On another machine (typically)
client = RtlSdrTcpClient(hostname='192.168.1.100', port=12345)
client.center_freq = 2e6
data = client.read_samples()
``` 


Ninguna de estas dos presentaron mejoras

### tcpclient.py

Está clase es la que se conecta al puerto abierto por `rtl_tcp` (1234). Decidí implementar asíncronamente la lectura de bytes y encolarlos en una `Queue` para que luego el `Producer` pueda transformarlos en data IQ. La idea es liberar lo más rapido posible el método `handle_read` así está disponible para el próximo buffer de bytes que lleguen al puerto TCP. 

```` python
class TCPClient(asyncore.dispatcher):
    # BUFF_SIZE = 8*1024
    BUFF_SIZE = 8*1024*1024

    def __init__(self, queue):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(('127.0.0.1', 1234))
        self.queue = queue

    def writable(self):
        return 0 # don't have anything to write

    def handle_connect(self):
        pass # connection succeeded

    def handle_expt(self):
        self.close() # connection failed, shutdown

    def handle_read(self):
        s = self.recv(self.BUFF_SIZE)
        #al conectarse con el dongle devuelve un string que no tengo que procesar
        if len(s)>15:
            self.queue.put(s)

    def handle_close(self):
        self.close()


def init(queue):
    client = TCPClient(queue)
    asyncore.loop()

````


## Demodulación

La parte más importante del trabajo sigue la estructura planteada en el enunciado, Python tiene librerías que tienen métodos muy parecidos a los de Matlab. Tanto el enunciado como el código son bien claros, se agregan algunas aclaraciones como comentarios

```python
import numpy as np
import scipy.signal as signal

FS = 2.048e6

def lpf_remez(freq,Fs):
	return signal.butter(4, freq / (Fs / 2), btype='low') # Con un butter de orden 4 conseguí buen tiempo y calidad

class Demodulador:

	def __init__(self,timer=None,plotter=None):
		self.F_bw1 = 180e3 #Ancho de banda FM comercial
		self.F_bw2 = 15e3 #Ancho de banda de la señal de audio
		self.N1 = int(FS//(self.F_bw1*2)) # Se redondea para abajo para
		self.N2 = int((FS/self.N1)//(self.F_bw2*2)) # no diezmar de más tal que Fs<2*BW
		self.primer_filtro = lpf_remez(self.F_bw1,FS)
		self.segundo_filtro = lpf_remez(self.F_bw2,(FS/self.N1))
		# También se calcula la frecuencia de muestreo final para configurar el reproductor
		self.output_Fs = int(FS / self.N1 / self.N2) 
		self.timer = timer
		self.plotter = plotter

	def lowpass(self,senial,filtro):
		return signal.lfilter(filtro[0],filtro[1], senial)

	def complex_array(self,data_array):
		data_array = np.frombuffer(data_array, dtype='uint8').astype(np.double)
		data_array = data_array - 127
		return data_array[0::2] + 1j*data_array[1::2]

	def decimate(self,senial,N):
		return signal.decimate(senial, N)

	def discriminar(self,senial):
		D = 5 # D = 75khz/15khz
		kf = D*self.F_bw1
		y = np.unwrap(np.angle(senial))/(2*np.pi*kf)
		y = np.diff(y)*FS
		y = y - np.mean(y)
		return y

	def outputFs(self):
		return self.output_Fs 

	def demodular(self,senial,toInt16 = False):
		self.plotter and self.plotter.clear()
		self.plotter and self.plotter.plotBoth(senial,'muestrada')
		
		self.timer and self.timer.tag('primer filtro')
		senial = self.lowpass(senial,self.primer_filtro)
		self.plotter and self.plotter.plotBoth(senial,'primer filtrado')
		
		self.timer and self.timer.tag('primer diezmado')
		senial = self.decimate(senial,self.N1)
		self.plotter and self.plotter.plotBoth(senial,'primer diezmado')
		
		self.timer and self.timer.tag('discriminado')
		senial = self.discriminar(senial)
		self.plotter and self.plotter.plotBoth(senial,'discriminado')

		self.timer and self.timer.tag('segundo filtro')
		senial = self.lowpass(senial,self.segundo_filtro)
		self.plotter and self.plotter.plotBoth(senial,'segundo filtro')

		self.timer and self.timer.tag('segundo diezmado')
		senial = self.decimate(senial,self.N2)
		self.plotter and self.plotter.plotBoth(senial,'segundo diezmado')

		self.timer and self.timer.tag('normalizado')
		senial = senial / np.max(np.abs(senial))

		if toInt16: return np.int16(senial* 32767) # Para la reproducción en tiempo real se necesita en 16bpm. (32767 = 2^15-1)
		return senial

```