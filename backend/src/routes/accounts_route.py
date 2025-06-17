"""
Route for managing accounts
Includes register and whoami.

Author: LunaLynx12
"""


from key_derivation import derive_dilithium_keypair, derive_kyber_keypair
from dilithium_py.dilithium import Dilithium2 as Dilithium
from blockchain import get_blockchain, create_transaction
from local_database import add_user, get_user_by_address
from mnemonics import generate_mnemonic_phrase
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from models import UserRegisterRequest
from kyber import generate_kyber_keys
from blockchain import get_blockchain
from local_database import DATABASE
from dilithium import sign_message
import sqlite3
import base64
import uuid

router = APIRouter()
bc = get_blockchain()

def generate_uid():
    return "0x" + uuid.uuid4().hex

@router.post("/register", description="Used for registering a new address on blockchain", tags=["Accounts"], summary="Register a new address")
async def register_user(user: UserRegisterRequest):
    """
    Auto-registers a user by generating their Dilithium keypair,
    and storing everything securely in the database.
    
    Only the public key is returned — private key is kept server-side for signing.
    """
    # Generate unique address
    address = generate_uid()
    mnemonic = generate_mnemonic_phrase(15)

    # Generate Dilithium keys
    public_key_bytes, secret_key_bytes = Dilithium.keygen()
    dilithium_pub_b64 = base64.b64encode(public_key_bytes).decode("utf-8")
    dilithium_priv_b64 = base64.b64encode(secret_key_bytes).decode("utf-8")

    # Generate Kyber keys
    kyber_pub, kyber_priv = generate_kyber_keys()
    kyber_pub_b64 = base64.b64encode(kyber_pub).decode("utf-8")
    kyber_priv_b64 = base64.b64encode(kyber_priv).decode("utf-8")

    # Store in DB
    add_user(
        address=address,
        dilithium_pub=dilithium_pub_b64,
        dilithium_priv=dilithium_priv_b64,
        kyber_pub=kyber_pub_b64,
        kyber_priv=kyber_priv_b64,
        mnemonic=mnemonic
    )

    # Sign registration transaction
    message_to_sign = f"REGISTER:{address}"
    signature_bytes = sign_message(secret_key_bytes, message_to_sign)
    signature_b64 = base64.b64encode(signature_bytes).decode("utf-8")

    timestamp = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DATABASE) as db:
        c = db.cursor()
        c.execute("""
            INSERT INTO messages (
                sender, 
                receiver, 
                   content, 
                   timestamp, 
                   signature, 
                   ciphertext
               ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "SYSTEM",
            "public",
            message_to_sign,
            timestamp,
            signature_b64,
            ""
        ))
        db.commit()

    # Create and add to mempool
    tx = create_transaction(
        tx_type="REGISTER",
        sender=address,
        receiver="",
        data={
            "dilithium_pub": dilithium_pub_b64,
            "kyber_pub": kyber_pub_b64,
            "signature": signature_b64
        }
    )
    if not bc.add_transaction(tx):
        raise HTTPException(status_code=400, detail="Too many transactions in pool")

    return {
        "status": "success",
        "user_id": address,
        "mnemonic": mnemonic,
        "dilithium_priv": dilithium_priv_b64,
        "kyber_priv": kyber_priv_b64
    }

@router.post("/whoami/{address}", description="Used for retriving a user from blockchain", tags=["Accounts"], summary="Check an existing address")
async def whoami(address: str):
    result = get_user_by_address(address)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove the dilithium_priv field from the response
    if "dilithium_priv" in result:
        del result["dilithium_priv"]
    
    return result

# TODO: fix and implement
@router.post("/recover", tags=["Accounts"])
async def recover_account(mnemonic: str):
    try:
        # Re-derive keys from mnemonic
        d_pub, d_priv = derive_dilithium_keypair(mnemonic)
        k_pub, k_priv = derive_kyber_keypair(mnemonic)

        # Return base64-encoded versions
        return {
            "status": "success",
            "dilithium_pub": base64.b64encode(d_pub).decode(),
            "kyber_pub": base64.b64encode(k_pub).decode()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recovery failed: {str(e)}")