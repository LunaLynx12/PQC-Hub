"""
dilithium.py

Provides utilities for signing and verifying messages using CRYSTALS-Dilithium,
as well as hashing messages for blockchain storage.

Author: LunaLynx12
"""

import base64
import hashlib
from dilithium_py.dilithium import Dilithium2 as Dilithium


# --- Message Hashing ---

def hash_message(message: str) -> str:
    """
    Returns the SHA-256 hash of the given message string.

    @param message: The message content to hash.
    @return: Hex-encoded SHA-256 hash.
    """
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


# --- Signing & Verification ---

def sign_message(secret_key: bytes, message: str) -> bytes:
    """
    Signs a message using the provided Dilithium secret key.
    
    @param secret_key: Dilithium private key (bytes)
    @param message: Message to sign (str)
    @return: Signature in raw bytes
    """
    message_bytes = message.encode("utf-8")
    return Dilithium.sign(secret_key, message_bytes)
    

def verify_signature(public_key: bytes, message: str, signature_b64: str) -> bool:
    """
    Verifies a Dilithium signature for a given message.

    @param public_key: Dilithium public key (bytes).
    @param message: Original message that was signed.
    @param signature_b64: Base64-encoded signature string.
    @return: True if valid, False otherwise.
    """
    try:
        message_bytes = message.encode("utf-8")
        signature_bytes = base64.b64decode(signature_b64)
        return Dilithium.verify(public_key, message_bytes, signature_bytes)
    except Exception as e:
        print(f"[!] Signature verification error: {e}")
        return False


# --- Key Utilities ---

def save_key(filename: str, key: bytes) -> None:
    """
    Saves a key (public or private) to disk in Base64 format.

    @param filename: Path to file where key should be saved.
    @param key: Key data in raw bytes.
    """
    with open(filename, "wb") as f:
        f.write(base64.b64encode(key))


def load_key(filename: str) -> bytes:
    """
    Loads a key (public or private) from disk.

    @param filename: Path to key file.
    @return: Key data in raw bytes.
    """
    try:
        with open(filename, "rb") as f:
            return base64.b64decode(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Key file not found: {filename}")