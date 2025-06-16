import asyncio
import websockets
from typing import Set, Tuple, Dict
import sys

# Local imports
from peer_discovery import PeerDiscovery
from protocol import MessageTypes, deserialize_peer_list

class P2PNode:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: Set[Tuple[str, int]] = set()  # (ip, port)
        self.connected_websockets: Dict[Tuple[str, int], websockets.WebSocketClientProtocol] = dict()
        self.failed_connections: Set[Tuple[str, int]] = set()
        self.server = None
        self.discovery = PeerDiscovery(self)

    async def start(self):
        """Start the WebSocket server"""
        self.server = await websockets.serve(
            self.handle_connection,
            self.host,
            self.port
        )
        print(f"Node running on ws://{self.host}:{self.port}")

    async def handle_connection(self, websocket):
        peer_address = websocket.remote_address[:2]
        ip, port = peer_address
        print(f"New connection from {ip}:{port}")
        self.peers.add((ip, port))
        self.connected_websockets[(ip, port)] = websocket

        try:
            # Start message sender
            asyncio.create_task(self.send_messages(ip, port, websocket))

            async for message in websocket:
                await self.process_message(message, websocket)
        finally:
            print(f"Connection closed with {ip}:{port}")
            self.connected_websockets.pop((ip, port), None)
            self.peers.discard((ip, port))

    async def process_message(self, message: bytes, websocket):
        if not message:
            print("Empty message received")
            return

        if len(message) < 1:
            print("Message too short")
            return

        msg_type = message[0]

        if msg_type == MessageTypes.PEER_LIST:
            try:
                peers = deserialize_peer_list(message)
                print("Received PEER_LIST:", peers)
                for peer in peers:
                    if peer not in self.peers:
                        asyncio.create_task(self.connect_to_peer(*peer))
            except Exception as e:
                print("Failed to parse PEER_LIST:", e)

        elif msg_type == MessageTypes.TEXT_MSG:
            if len(message) >= 5:
                count = int.from_bytes(message[1:5], 'big')
                print(f"Received TEXT_MSG with value: {count}")
            else:
                print("TEXT_MSG message too short")

        else:
            print(f"Unknown binary message type {hex(msg_type)}, length {len(message)}")

    async def send_messages(self, ip: str, port: int, websocket):
        count = 1
        while True:
            try:
                # Format: [TYPE][COUNT AS 4 BYTES][TEXT PAYLOAD]
                text = f"Hello from {self.port} - {count}"
                payload = count.to_bytes(4, 'big') + text.encode('utf-8')
                msg = bytes([MessageTypes.TEXT_MSG]) + payload

                await websocket.send(msg)
                print(f"Sent to {ip}:{port} -> {text}")
                count += 1
                await asyncio.sleep(3)
            except Exception as e:
                print(f"Lost connection to {ip}:{port}: {e}")
                self.connected_websockets.pop((ip, port), None)
                self.peers.discard((ip, port))
                break

    async def connect_to_peer(self, peer_ip: str, peer_port: int):
        uri = f"ws://{peer_ip}:{peer_port}"
        if (peer_ip, peer_port) in self.connected_websockets or (peer_ip, peer_port) in self.failed_connections:
            return  # Already connected or already failed

        print(f"Connecting to {peer_ip}:{peer_port}...")
        try:
            async with websockets.connect(uri) as ws:
                
                self.peers.add((peer_ip, peer_port))
                self.connected_websockets[(peer_ip, peer_port)] = ws
                self.failed_connections.discard((peer_ip, peer_port))

                # Start sending messages
                asyncio.create_task(self.send_messages(peer_ip, peer_port, ws))

                # Wait for messages
                async for message in ws:
                    await self.process_message(message, ws)
        except Exception as e:
            print(f"Failed to connect to {uri}: {e}")
            self.failed_connections.add((peer_ip, peer_port))

    async def scan_for_peers(self, ip="127.0.0.1", port_range=range(8760, 8770)):
        """Scan for nodes on given IP address and port range"""
        while True:
            print("Scanning for peers...")
            for port in port_range:
                if (ip, port) not in self.peers and port != self.port:
                    asyncio.create_task(self.connect_to_peer(ip, port))
            await asyncio.sleep(10)  # Scan every 10 seconds


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Port must be an integer")
        sys.exit(1)

    print(f"Running node.py v3.0 on port {port}")

    async def main():
        node = P2PNode("127.0.0.1", port)
        await node.start()

        # Background tasks
        asyncio.create_task(node.scan_for_peers())
        asyncio.create_task(node.discovery.share_peers())

        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("Shutting down node...")

    asyncio.run(main())