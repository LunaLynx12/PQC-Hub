from blockchain import get_blockchain
from config import KNOWN_PEERS
from fastapi import APIRouter
import asyncio


router = APIRouter()
bc = get_blockchain()

async def fetch_remote_chain(peer_url: str):
    """Fetches the blockchain from a remote peer."""
    try:
        print("STUB fetching blockchain...")
    except Exception as e:
        print(f"[Sync] Failed to fetch chain from {peer_url}: {e}")
    return None

async def broadcast_chain_to_peers():
    """Broadcasts local chain to all known peers for synchronization."""
    chain_payload = {"chain": bc.chain}
    print("STUB broadcating chain to peers...")

@router.post("/sync", tags=["P2P"])
async def sync_with_peer(peer_url: str):
    """
    Syncs with one peer by fetching their chain and applying it if valid.
    """
    remote_chain = await fetch_remote_chain(peer_url)
    if remote_chain:
        if bc.validate_chain(remote_chain):
            if len(remote_chain) > len(bc.chain):
                print(f"[Sync] Replacing chain with longer one from {peer_url}")
                bc.replace_chain(remote_chain)
            else:
                print(f"[Sync] Remote chain from {peer_url} is not longer. Skipping.")
        else:
            print(f"[Sync] Received invalid chain from {peer_url}")
    else:
        print(f"[Sync] No chain received from {peer_url}")

@router.post("/sync-all", tags=["P2P"])
async def full_sync_endpoint():
    """
    Synchronizes the local blockchain with all known peers.
    - Fetches each peer's chain
    - Validates and replaces local chain if necessary
    - Broadcasts local chain back to peers
    """
    tasks = [fetch_and_apply_chain(peer) for peer in KNOWN_PEERS]
    await asyncio.gather(*tasks)

    await broadcast_chain_to_peers()

    return {
        "status": "success",
        "action": "full_sync_complete",
        "known_peers": KNOWN_PEERS,
        "local_chain_length": len(bc.chain),
    }

async def fetch_and_apply_chain(peer_url: str):
    """Fetch and validate chain from a single peer."""
    remote_chain = await fetch_remote_chain(peer_url)
    if remote_chain and bc.validate_chain(remote_chain):
        if len(remote_chain) > len(bc.chain):
            print(f"[Sync] Replacing chain from {peer_url}")
            bc.replace_chain(remote_chain)
        else:
            print(f"[Sync] Chain from {peer_url} is not longer. Skipping.")
    else:
        print(f"[Sync] Invalid chain from {peer_url}")