from dilithium_py.dilithium import Dilithium2 as Dilithium
from blockchain import get_blockchain, create_transaction
from local_database import add_user, get_user_by_address
from fastapi import APIRouter, HTTPException
from models import UserRegisterRequest
from kyber import generate_kyber_keys
from blockchain import get_blockchain
from dilithium import sign_message
import base64


router = APIRouter()
bc = get_blockchain()

# TODO: assign random uid addresses for register, replace message from User 0x1234567891 added to memory pool. top only give the uid
# TODO: register to be Unique
# TODO: on register send private keys
# TODO: read chain using ws
# TODO: decrypt and store private messages

@router.post("/register", description="Used for registering a new address on blockchain", tags=["Accounts"], summary="Register a new address")
async def register_user(user: UserRegisterRequest):
    """
    Auto-registers a user by generating their Dilithium keypair,
    and storing everything securely in the database.
    
    Only the public key is returned — private key is kept server-side for signing.
    """

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
        address=user.address,
        dilithium_pub=dilithium_pub_b64,
        dilithium_priv=dilithium_priv_b64,
        kyber_pub=kyber_pub_b64,
        kyber_priv=kyber_priv_b64
    )

    # Sign registration transaction
    message_to_sign = f"REGISTER:{user.address}"
    signature_bytes = sign_message(secret_key_bytes, message_to_sign)
    signature_b64 = base64.b64encode(signature_bytes).decode("utf-8")

    # Create and add to mempool
    tx = create_transaction(
        tx_type="REGISTER",
        sender=user.address,
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
        "message": f"User {user.address} added to memory pool.",
        "dilithium_pub": dilithium_pub_b64,
        "kyber_pub": kyber_pub_b64
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