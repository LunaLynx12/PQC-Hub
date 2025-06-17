"""
Route for Reading data from blockchain

Author: LunaLynx12
"""


from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from blockchain import get_blockchain
import json
from local_database import get_all_messages_from_db

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
        # Load initial data from both blockchain and database
        chain_data = [block.model_dump() for block in bc.chain]
        messages_data = [msg.model_dump() for msg in get_all_messages_from_db()]

        # Send combined data
        initial_data = {
            "type": "INITIAL_CHAIN",
            "data": {
                "chain": chain_data,
                "messages": messages_data
            }
        }

        await websocket.send_text(json.dumps(initial_data))

        # Register subscriber
        bc.add_subscriber(websocket)
        
        # Keep connection open
        while True:
            try:
                # Optional: receive text if needed
                await websocket.receive_text()
            except Exception:
                break

        # Unregister on disconnect
        bc.remove_subscriber(websocket)
    except WebSocketDisconnect:
        bc.remove_subscriber(websocket)
        print("[WebSocket] Client disconnected")