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