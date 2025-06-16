from dilithium_py.dilithium import Dilithium2 as Dilithium
from encryption import aes_encrypt, aes_decrypt
from fastapi import APIRouter, HTTPException
from kyber import generate_kyber_keys
from config import TEST_KEY
import base64

router = APIRouter()

@router.get("/aes-test", description="Used for testing", deprecated=True, tags=["Testing"], summary="Test aes encryption and decryption")
async def aes_test(message: str):
    try:
        # Encrypt
        encrypted_data, ciphertext_only = aes_encrypt(TEST_KEY, message)
        
        # Decrypt
        decrypted = aes_decrypt(TEST_KEY, encrypted_data)
        
        return {
            "original_message": message,
            "encrypted_data": encrypted_data.hex(),  # Convert bytes to hex for JSON
            "ciphertext_only": ciphertext_only.hex(),
            "decrypted_message": decrypted,
            "status": "Success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Encryption/Decryption failed: {str(e)}")

@router.get("/generate-dilithium-keys", description="Used for testing", deprecated=True, tags=["Testing"], summary="Test dilithium key generation")
async def generate_keys():
    """
    Generates a new Dilithium keypair and returns them in Base64 format.
    """
    public_key, secret_key = Dilithium.keygen()
    
    return {
        "dilithium_pub": base64.b64encode(public_key).decode("utf-8"),
        "dilithium_priv": base64.b64encode(secret_key).decode("utf-8")
    }

@router.get("/generate-kyber512-keys", description="Used for testing", deprecated=True, tags=["Testing"], summary="Test kyber key generation")
async def generate_keys():
    """
    Generates a new Kyber keypair and returns them in Base64 format.
    """
    kyber_pub, kyber_priv = generate_kyber_keys()
    
    return {
        "kyber_pub": base64.b64encode(kyber_pub).decode("utf-8"),
        "kyber_priv": base64.b64encode(kyber_priv).decode("utf-8")
    }