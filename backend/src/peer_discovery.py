import asyncio
from protocol import serialize_peer_list, MessageTypes

class PeerDiscovery:
    def __init__(self, node):
        self.node = node

    async def share_peers(self):
        """Periodically exchange the list of actively connected peers"""
        while True:
            if self.node.connected_websockets:
                valid_ports = set(range(8760, 8770))  # Optional: restrict port range

                # 🔄 Use only actively connected peers
                peers_to_share = [
                    (ip, port) for (ip, port) in self.node.connected_websockets.keys()
                    if port in valid_ports and (ip, port) != (self.node.host, self.node.port)
                ]

                raw_data = serialize_peer_list(peers_to_share)
                msg = bytes([MessageTypes.PEER_LIST]) + raw_data[1:]  # Skip double type byte
                await self.broadcast(msg)

            await asyncio.sleep(5)



    async def broadcast(self, message: bytes):
        """Send to all connected peers using existing WebSocket connections"""
        disconnected = set()

        for (ip, port), ws in list(self.node.connected_websockets.items()):
            if (ip, port) == (self.node.host, self.node.port):
                continue
            try:
                await ws.send(message)
            except Exception:
                disconnected.add((ip, port))

        # Clean up disconnected peers
        for dead in disconnected:
            print(f"Removing disconnected peer: {dead}")
            self.node.connected_websockets.pop(dead, None)
            self.node.peers.discard(dead)

class MessageTypes:
    PEER_LIST = 0x01
    TEXT_MSG = 0x02

def serialize_peer_list(peers: list) -> bytes:
    """Format: [TYPE:1][COUNT:1][IP:4][PORT:2]..."""
    msg = bytes([MessageTypes.PEER_LIST, len(peers)])
    for ip, port in peers:
        msg += bytes(map(int, ip.split('.'))) + port.to_bytes(2, 'big')
    return msg

def deserialize_peer_list(data: bytes) -> list:
    """Parse peer list messages"""
    count = data[1]
    peers = []
    for i in range(count):
        start = 2 + i * 6
        ip = ".".join(map(str, data[start:start+4]))
        port = int.from_bytes(data[start+4:start+6], 'big')
        peers.append((ip, port))
    return peers