import asyncio
import websockets
from typing import Set, Tuple, Dict, List
import hashlib
import json
import time
from peer_discovery import PeerDiscovery
from protocol import MessageTypes, deserialize_peer_list


class Block:
    def __init__(self, index: int, timestamp: float, data: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Now a list of dictionaries
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }

    @staticmethod
    def from_dict(block_data):
        block = Block(
            block_data['index'],
            block_data['timestamp'],
            block_data['data'],  # now expects a list of dicts
            block_data['previous_hash']
        )
        block.hash = block_data['hash']
        return block


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), [{"id": 0, "content": "Genesis Block", "author": "System"}], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block: Block):
        self.chain.append(new_block)
        print(f"Block added: {new_block.index} | Entries: {len(new_block.data)} | Hash: {new_block.hash}")
        return True

    def replace_chain(self, new_chain: List[Block]):
        if len(new_chain) > len(self.chain) and self.validate_chain(new_chain):
            self.chain = new_chain
            print("Chain replaced.")
            return True
        return False

    def validate_chain(self, chain: List[Block]) -> bool:
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


class MessageTypesExtended(MessageTypes):
    NEW_BLOCK = 0x03
    BLOCKCHAIN_REQUEST = 0x04
    BLOCKCHAIN_RESPONSE = 0x05
    GET_BLOCK_BY_INDEX = 0x06
    BLOCK_RESPONSE = 0x07


def serialize_block(block: Block) -> bytes:
    json_data = json.dumps(block.to_dict())
    return bytes([MessageTypesExtended.NEW_BLOCK]) + json_data.encode('utf-8')


def deserialize_block(data: bytes) -> Block:
    json_str = data[1:].decode('utf-8')
    block_data = json.loads(json_str)
    return Block.from_dict(block_data)


def serialize_blockchain(chain: List[Block]) -> bytes:
    json_data = json.dumps([block.to_dict() for block in chain])
    return bytes([MessageTypesExtended.BLOCKCHAIN_RESPONSE]) + json_data.encode('utf-8')


def deserialize_blockchain(data: bytes) -> List[Block]:
    json_str = data[1:].decode('utf-8')
    block_dicts = json.loads(json_str)
    return [Block.from_dict(bd) for bd in block_dicts]


class P2PNode:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: Set[Tuple[str, int]] = set()
        self.connected_websockets: Dict[Tuple[str, int], websockets.WebSocketClientProtocol] = dict()
        self.failed_connections: Set[Tuple[str, int]] = set()
        self.server = None
        self.discovery = PeerDiscovery(self)
        self.blockchain = Blockchain()

    async def start(self):
        self.server = await websockets.serve(self.handle_connection, self.host, self.port)
        print(f"P2P Node running on ws://{self.host}:{self.port}")

    async def handle_connection(self, websocket):
        peer_address = websocket.remote_address[:2]
        ip, port = peer_address
        print(f"Accepted connection from {ip}:{port}")
        self.peers.add((ip, port))
        self.connected_websockets[(ip, port)] = websocket
        try:
            asyncio.create_task(self.send_messages(ip, port, websocket))
            async for message in websocket:
                await self.process_message(message, websocket)
        except websockets.ConnectionClosed:
            pass
        finally:
            print(f"Connection closed with {ip}:{port}")
            self.connected_websockets.pop((ip, port), None)
            self.peers.discard((ip, port))

    async def process_message(self, message: bytes, websocket):
        if not message:
            return
        msg_type = message[0]
        if msg_type == MessageTypes.PEER_LIST:
            try:
                peers = deserialize_peer_list(message)
                for peer in peers:
                    if peer not in self.peers and peer != (self.host, self.port):
                        asyncio.create_task(self.connect_to_peer(*peer))
            except Exception as e:
                print("Failed to parse PEER_LIST:", e)
        elif msg_type == MessageTypes.TEXT_MSG:
            pass
        elif msg_type == MessageTypesExtended.NEW_BLOCK:
            try:
                block = deserialize_block(message)
                # Ensure the data is a simple dictionary, not a list of blocks
                if isinstance(block.data, list):
                    print("Received block contains nested blocks. Ignoring.")
                # Validate the block
                if all(b.hash != block.hash for b in self.blockchain.chain):
                    self.blockchain.add_block(block)
                    await self.broadcast(message, exclude_ws=websocket)
                else:
                    print(f"Duplicate block ignored: {block.index}")
            except Exception as e:
                print(f"Failed to process NEW_BLOCK: {e}")
        elif msg_type == MessageTypesExtended.GET_BLOCK_BY_INDEX:
            try:
                index = int.from_bytes(message[1:], 'big')
                if 0 <= index < len(self.blockchain.chain):
                    block = self.blockchain.chain[index]
                    block_msg = serialize_block(block)
                    await websocket.send(block_msg)
                else:
                    await websocket.send(bytes([MessageTypesExtended.BLOCK_RESPONSE]) + b'Block not found')
            except Exception as e:
                print(f"Error getting block by index: {e}")
        elif msg_type == MessageTypesExtended.BLOCKCHAIN_REQUEST:
            full_chain = serialize_blockchain(self.blockchain.chain)
            await websocket.send(full_chain)
        elif msg_type == MessageTypesExtended.BLOCKCHAIN_RESPONSE:
            try:
                new_chain = deserialize_blockchain(message)
                print("Replacing local blockchain with received one")
                self.blockchain.replace_chain(new_chain)
            except Exception as e:
                print("Failed to process BLOCKCHAIN_RESPONSE:", e)

    async def send_messages(self, ip: str, port: int, websocket):
        count = 1
        while True:
            try:
                text = f"Hello from {self.port} - {count}"
                payload = count.to_bytes(4, 'big') + text.encode('utf-8')
                msg = bytes([MessageTypes.TEXT_MSG]) + payload
                await websocket.send(msg)
                count += 1
                await asyncio.sleep(3)
            except Exception:
                self.connected_websockets.pop((ip, port), None)
                self.peers.discard((ip, port))
                break

    def create_new_block(self, data: dict) -> Block:
        """Create a new block with user-provided content."""
        latest_block = self.blockchain.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=time.time(),
            data=[data],  # Only accept user content here
            previous_hash=latest_block.hash
        )
        self.blockchain.add_block(new_block)
        return new_block

    async def broadcast(self, message: bytes, exclude_ws=None):
        disconnected = set()
        for (ip, port), ws in list(self.connected_websockets.items()):
            if ws == exclude_ws:
                continue
            try:
                await ws.send(message)
            except Exception:
                disconnected.add((ip, port))
        for dead in disconnected:
            self.connected_websockets.pop(dead, None)
            self.peers.discard(dead)

    async def connect_to_peer(self, peer_ip: str, peer_port: int):
        uri = f"ws://{peer_ip}:{peer_port}"
        if (peer_ip, peer_port) in self.connected_websockets or (peer_ip, peer_port) in self.failed_connections or (peer_ip, peer_port) == (self.host, self.port):
            return
        try:
            ws = await websockets.connect(uri)
            self.peers.add((peer_ip, peer_port))
            self.connected_websockets[(peer_ip, peer_port)] = ws
            self.failed_connections.discard((peer_ip, peer_port))
            await asyncio.sleep(1)
            await ws.send(bytes([MessageTypesExtended.BLOCKCHAIN_REQUEST]))
            asyncio.create_task(self.send_messages(peer_ip, peer_port, ws))
            async def listen():
                try:
                    async for message in ws:
                        await self.process_message(message, ws)
                except websockets.ConnectionClosed:
                    pass
                finally:
                    self.connected_websockets.pop((peer_ip, peer_port), None)
                    self.peers.discard((peer_ip, peer_port))
            asyncio.create_task(listen())
        except Exception as e:
            self.failed_connections.add((peer_ip, peer_port))

    async def scan_for_peers(self, ip="127.0.0.1", port_range=range(8760, 8770)):
        while True:
            for port in port_range:
                if (ip, port) not in self.peers and port != self.port:
                    asyncio.create_task(self.connect_to_peer(ip, port))
            await asyncio.sleep(10)