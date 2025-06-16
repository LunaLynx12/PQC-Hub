from fastapi import APIRouter
from blockchain import get_blockchain

router = APIRouter()
bc = get_blockchain()

@router.post("/chain", tags=["Blockchain"])
async def get_chain():
    """
    Returns the current state of the local blockchain.

    @return: JSON object containing the full chain.
    """
    return {"chain": [block.model_dump() for block in bc.chain]}