from rtlsdr.rtlsdrtcp.server import RtlSdrTcpServer
server = RtlSdrTcpServer(hostname='127.0.0.1', port=12345)
server.run_forever()