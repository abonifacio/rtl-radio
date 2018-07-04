const { spawn } = require('child_process');
const fs = require('fs');

const demodulador = spawn('python',['fm-stdout.py'])
const fmedia = spawn('fmedia',['@stdin.wav', '--rate=44100','--channels=mono','--format=float32'])

const file = fs.createWriteStream('muestras.log')
demodulador.stdout.pipe(file)

// child.stdout.on('data', (data) => {
//   console.log(`child stdout:\n${data}`);
// });