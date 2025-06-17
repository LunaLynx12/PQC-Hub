"""
Route for Reading data from blockchain

Author: LunaLynx12
"""


from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from blockchain import get_blockchain
import asyncio
import json

router = APIRouter()
bc = get_blockchain()

@router.post("/chain", tags=["Blockchain"])
async def get_chain():
    """
    Returns the current state of the local blockchain.

    @return: JSON object containing the full chain.
    """
    return {"chain": [block.model_dump() for block in bc.chain]}

@router.websocket("/ws/chain")
async def websocket_chain(websocket: WebSocket):
    await websocket.accept()
    
    try:
        # Send initial chain data
        initial_chain = [block.model_dump() for block in bc.chain]
        await websocket.send_text(json.dumps({"type": "INITIAL_CHAIN", "data": initial_chain}))

        # Register subscriber
        bc.add_subscriber(websocket)
        
        # Keep connection open
        while True:
            try:
                # Wait for any message from client (optional)
                await websocket.receive_text()
            except Exception:
                break

        # Unregister on disconnect
        bc.remove_subscriber(websocket)
    except WebSocketDisconnect:
        bc.remove_subscriber(websocket)
        print("[WebSocket] Client disconnected")