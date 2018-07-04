const dgram = require('dgram');

function createServer(PORT,onData){
	const server = dgram.createSocket('udp4');
	server.on('error', (err) => {
	  server.close();
	});
	
	server.on('message',onData);

	server.on('listening', () => {
	  const address = server.address();
	  console.log('UDP server corriendo',address);
	});

	server.bind(PORT);

}

var time = new Date().getTime();

createServer(8080,function(data){
	console.log('Muestras por segundo: ',data.length/((new Date().getTime()) - time));
	time = new Date().getTime();
});