from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from config import KNOWN_PEERS
import asyncio

# This will be set in main.py during startup
p2p_node = None
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(f"[WebSocket] Connection attempt from {websocket.client.host}:{websocket.client.port}")
    try:
        await websocket.accept()
        print(f"[WebSocket] Accepted connection from {websocket.client.host}:{websocket.client.port}")
        while True:
            data = await websocket.receive_text()
            print(f"[WebSocket] Received: {data} from {websocket.client.host}:{websocket.client.port}")
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        print(f"[WebSocket] Error with client {websocket.client.host}:{websocket.client.port}: {e}")
    finally:
        print(f"[WebSocket] Client {websocket.client.host}:{websocket.client.port} disconnected")

async def fetch_remote_chain(peer_url: str):
    """Fetches the blockchain from a remote peer."""
    ip, port = peer_url.split(":")
    # print(f"[Sync] Attempting to connect to peer at {ip}:{port}")
    try:
        await p2p_node.connect_to_peer(ip, int(port))
        return p2p_node.blockchain.chain
    except Exception as e:
        # print(f"[Sync] Failed to fetch chain from {peer_url}: {e}")
        return None

async def broadcast_chain_to_peers():
    """Broadcasts local chain to all known peers for synchronization."""
    chain_payload = {"chain": [block.to_dict() for block in p2p_node.blockchain.chain]}
    print("Broadcasting chain to peers...")
    # Implement broadcasting logic here if not already done

@router.post("/sync", tags=["P2P"])
async def sync_with_peer(peer_url: str):
    """
    Syncs with one peer by fetching their chain and applying it if valid.
    """
    # print(f"[Sync] Initiating sync with peer: {peer_url}")
    remote_chain = await fetch_remote_chain(peer_url)
    if remote_chain:
        if p2p_node.blockchain.validate_chain(remote_chain):
            if len(remote_chain) > len(p2p_node.blockchain.chain):
                print(f"[Sync] Replacing chain with longer one from {peer_url}")
                p2p_node.blockchain.replace_chain(remote_chain)
            else:
                pass
                # print(f"[Sync] Remote chain from {peer_url} is not longer. Skipping.")
        else:
            pass
            # print(f"[Sync] Received invalid chain from {peer_url}")
    else:
        pass
        # print(f"[Sync] No chain received from {peer_url}")
    return {"status": "success", "action": "sync_complete", "peer": peer_url}

@router.post("/sync-all", tags=["P2P"])
async def full_sync_endpoint():
    """
    Synchronizes the local blockchain with all known peers.
    - Fetches each peer's chain
    - Validates and replaces local chain if necessary
    - Broadcasts local chain back to peers
    """
    print("[Sync] Starting full sync with all known peers")
    tasks = [fetch_and_apply_chain(peer) for peer in KNOWN_PEERS]
    await asyncio.gather(*tasks)
    await broadcast_chain_to_peers()
    return {
        "status": "success",
        "action": "full_sync_complete",
        "known_peers": KNOWN_PEERS,
        "local_chain_length": len(p2p_node.blockchain.chain),
    }

async def fetch_and_apply_chain(peer_url: str):
    """Fetch and validate chain from a single peer."""
    # print(f"[Sync] Fetching chain from {peer_url}")
    remote_chain = await fetch_remote_chain(peer_url)
    if remote_chain and p2p_node.blockchain.validate_chain(remote_chain):
        if len(remote_chain) > len(p2p_node.blockchain.chain):
            # print(f"[Sync] Replacing chain from {peer_url}")
            p2p_node.blockchain.replace_chain(remote_chain)
        else:
            pass
            # print(f"[Sync] Chain from {peer_url} is not longer. Skipping.")
    else:
        pass
        # print(f"[Sync] Invalid chain from {peer_url}")