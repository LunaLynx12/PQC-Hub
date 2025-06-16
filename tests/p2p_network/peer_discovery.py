import random
import asyncio
from protocol import serialize_peer_list, MessageTypes

class PeerDiscovery:
    def __init__(self, node):
        self.node = node

    async def share_peers(self):
        """Periodically exchange peer lists"""
        while True:
            if self.node.peers:
                peers_to_share = random.sample(
                    list(self.node.peers),
                    min(3, len(self.node.peers))
                )
                raw_data = serialize_peer_list(peers_to_share)
                msg = bytes([MessageTypes.PEER_LIST]) + raw_data[1:]  # Add message type header
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