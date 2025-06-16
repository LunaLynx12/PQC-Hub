"""
Provides utilities for signing and verifying messages using CRYSTALS-Dilithium,
as well as hashing messages for blockchain storage.

Author: LunaLynx12
"""

from dilithium_py.dilithium import Dilithium2 as Dilithium
import hashlib
import base64


def hash_message(message: str) -> str:
    """
    Returns the SHA-256 hash of the given message string.

    @param message: The message content to hash.
    @return: Hex-encoded SHA-256 hash.
    """
    return hashlib.sha256(message.encode("utf-8")).hexdigest()

def sign_message(secret_key: bytes, message: str) -> bytes:
    """
    Signs a message using the provided Dilithium private key.

    param secret_key: Dilithium secret key (in raw bytes)
    type secret_key: bytes
    param message: Message to be signed
    type message: str
    return: Raw signature bytes
    rtype: bytes
    """
    message_bytes = message.encode("utf-8")
    return Dilithium.sign(secret_key, message_bytes)
    
def verify_signature(public_key: bytes, message: str, signature_b64: str) -> bool:
    """
    Verifies a Dilithium digital signature against a message.

    param public_key: Dilithium public key (in raw bytes)
    type public_key: bytes
    param message: Original message that was signed
    type message: str
    param signature_b64: Base64-encoded signature string
    type signature_b64: str
    return: True if the signature is valid, False otherwise
    rtype: bool
    raises Exception: Prints error message if verification fails unexpectedly
    """
    try:
        message_bytes = message.encode("utf-8")
        signature_bytes = base64.b64decode(signature_b64)
        return Dilithium.verify(public_key, message_bytes, signature_bytes)
    except Exception as e:
        print(f"[!] Signature verification error: {e}")
        return False

def save_key(filename: str, key: bytes) -> None:
    """
    Saves a cryptographic key (public or private) to disk in Base64 format.

    param filename: Path to the file where the key will be saved
    type filename: str
    param key: Key data in raw bytes
    type key: bytes
    return: None
    """
    with open(filename, "wb") as f:
        f.write(base64.b64encode(key))

def load_key(filename: str) -> bytes:
    """
    Loads a cryptographic key (public or private) from disk.

    param filename: Path to the key file
    type filename: str
    return: Key data in raw bytes
    rtype: bytes
    raises FileNotFoundError: If the specified file does not exist
    """
    try:
        with open(filename, "rb") as f:
            return base64.b64decode(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Key file not found: {filename}")