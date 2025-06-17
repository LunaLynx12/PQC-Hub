"""
Route for sending messages to the blockchain

Author: LunaLynx12
"""


from local_database import get_user_by_address, DATABASE
from dilithium import sign_message, hash_message
from fastapi import APIRouter, HTTPException
from blockchain import create_transaction
from datetime import datetime, timezone
from blockchain import get_blockchain
from kyber import generate_shared_key
from encryption import aes_encrypt
from typing import Optional
from models import Message
import sqlite3
import base64


router = APIRouter()
bc = get_blockchain()

def get_dilithium_secret_key(sender_address: str) -> bytes:
    result = get_user_by_address(sender_address)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dilithium_priv_b64 = result.get("dilithium_priv")
    if not dilithium_priv_b64:
        raise HTTPException(status_code=500, detail="Private key missing from DB")
    try:
        return base64.b64decode(dilithium_priv_b64)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to decode private key: {str(e)}")

@router.post("/send", response_model=Message, tags=["Message"])
async def send_message(msg: Message):
    """
    Sends a message to another user.

    If receiver is 'public', message goes into blockchain.
    If private, message is encrypted using Kyber + AES-GCM.
    All messages are signed using Dilithium.

    @param msg: Message object containing sender, receiver, content, timestamp
    @return: The same message after processing
    """
    try:
        # Step 1: Get sender keys
        secret_key = get_dilithium_secret_key(msg.sender)
        sender_data = get_user_by_address(msg.sender)
        if not sender_data:
            raise HTTPException(status_code=404, detail="Sender not found")
        dilithium_pub_b64 = sender_data.get("dilithium_pub")
        if not dilithium_pub_b64:
            raise HTTPException(status_code=500, detail="Public key missing from DB")

        # Step 2: Sign message_hash instead of raw content
        msg_hash = hash_message(msg.content)
        signature_bytes = sign_message(secret_key, msg_hash)
        signature_b64 = base64.b64encode(signature_bytes).decode("utf-8")

        # Step 3: Handle encryption for private messages
        encrypted_content: Optional[str] = None
        ciphertext_b64: Optional[str] = None

        if msg.receiver != "public":
            recipient_data = get_user_by_address(msg.receiver)
            if not recipient_data:
                raise HTTPException(status_code=404, detail="Recipient not found")
            kyber_pub_b64 = recipient_data.get("kyber_pub")
            if not kyber_pub_b64:
                raise HTTPException(status_code=400, detail="Recipient has no Kyber public key")
            kyber_pub_bytes = base64.b64decode(kyber_pub_b64)
            shared_key, ciphertext_data = generate_shared_key(kyber_pub_bytes)
            encrypted_payload = aes_encrypt(shared_key, msg.content)
            encrypted_content = base64.b64encode(encrypted_payload).decode("utf-8")
            ciphertext_b64 = base64.b64encode(ciphertext_data).decode("utf-8")
        else:
            encrypted_content = msg.content  # Public message doesn't need encryption

        # Step 4: Save message to database
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
                msg.sender,
                msg.receiver,
                encrypted_content or "",
                timestamp,
                signature_b64,
                ciphertext_b64 or ""
            ))
            db.commit()

        # Step 5: Add to blockchain if public
        tx_data = {
            "message_hash": msg_hash,
            "signature": signature_b64,
            "dilithium_pub": dilithium_pub_b64,
        }

        if msg.receiver == "public":
            tx_data["message"] = msg.content

        if msg.receiver != "public":
            tx_data["ciphertext"] = encrypted_content
            tx_data["kyber_ciphertext"] = ciphertext_b64

        tx = create_transaction(
            tx_type="PRIVATE_MESSAGE" if msg.receiver != "public" else "PUBLIC_MESSAGE",
            sender=msg.sender,
            receiver=msg.receiver,
            data=tx_data
        )

        if not bc.add_transaction(tx):
            raise HTTPException(status_code=400, detail="Mempool full — cannot add transaction now.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Message failed: {str(e)}")

    return msg