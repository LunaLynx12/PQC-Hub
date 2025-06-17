"""
Route for checking the current pool and validating it using PoA

Author: LunaLynx12
"""


from fastapi import APIRouter, HTTPException
from blockchain import get_blockchain

bc = get_blockchain()
router = APIRouter()

@router.get("/validate", description="Used for PoA validation", tags=["Validation"], summary="Validate the mempool")
async def validate_block(validator: str):
    """
    Allows a validator to propose and commit a new block from pending transactions.
    """
    new_block = bc.mine_block(validator)

    if new_block is None:
        raise HTTPException(status_code=403, detail="Validator not authorized or no pending transactions")

    return {
        "status": "success",
        "block": new_block.model_dump()
    }

@router.get("/mempool", description="Used for checking the mempool", tags=["Validation"], summary="Check the mempool")
async def get_pending_transactions():
    return {
        "pending_count": len(bc.pending_transactions),
        "pending": [dict(t) for t in bc.pending_transactions]
    }