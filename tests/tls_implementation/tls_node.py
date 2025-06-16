import ssl
import asyncio
from pathlib import Path
from websockets.server import serve
from websockets.client import connect

class TLSNode:
    def __init__(self, host: str, port: int, cert_path: str):
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_context.load_cert_chain(cert_path / 'cert.pem', cert_path / 'key.pem')
        self.host = host
        self.port = port

    async def start_server(self):
        async with serve(
            self.handle_connection,
            'localhost',  # Changed from IP to hostname
            self.port,
            ssl=self.ssl_context
        ):
            print(f"TLS Node running on wss://localhost:{self.port}")
            await asyncio.Future()

    @staticmethod
    async def connect_to(host: str, port: int, cert_path: str):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.load_verify_locations(cert_path / 'ca.pem')
        
        # Disable hostname verification for testing
        ssl_context.check_hostname = False
        
        async with connect(
            f"wss://{host}:{port}",
            ssl=ssl_context
        ) as websocket:
            await websocket.send("Hello TLS World!")
            response = await websocket.recv()
            print(f"Server response: {response}")
            
    async def handle_connection(self, websocket):
        """Secure message handler"""
        peer = websocket.remote_address
        print(f"Secure connection from {peer}")
        async for message in websocket:
            print(f"Secure message: {message}")
            await websocket.send(f"Secure ACK: {message}")