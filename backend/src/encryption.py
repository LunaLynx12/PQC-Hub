"""
Implements AES-GCM symmetric encryption using shared key from Kyber.
Used to encrypt/decrypt messages after establishing a shared secret via Kyber.

Author: LunaLynx12
"""


from Crypto.Cipher import AES

def aes_encrypt(key: bytes, plaintext: str) -> bytes:
    """
    Encrypts a plaintext string using AES-GCM with a shared key.

    The output includes the nonce, ciphertext, and authentication tag,
    formatted as: `nonce (16B) + ciphertext + tag (16B)`.

    param key: Shared symmetric key (typically 32 bytes)
    type key: bytes
    param plaintext: String message to encrypt
    type plaintext: str
    return: Encrypted data blob containing nonce + ciphertext + tag
    rtype: bytes
    """
    cipher = AES.new(key[:32], AES.MODE_GCM)
    cipher.update(b"header")
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return cipher.nonce + tag + ciphertext

def aes_decrypt(key: bytes, data: bytes) -> str:
    """
    Decrypts an AES-GCM encrypted message using the shared key.

    Data structure expected: `nonce (16B) + ciphertext + tag (16B)`.

    param key: Shared symmetric key (32 bytes)
    type key: bytes
    param data: Encrypted data blob
    type data: bytes
    return: Decrypted plaintext string
    rtype: str
    raises ValueError: If decryption fails due to invalid tag or corrupted data
    """
    try:
        nonce = data[:16]
        ciphertext = data[16:-16]
        tag = data[-16:]

        cipher = AES.new(key[:32], AES.MODE_GCM, nonce=nonce)
        cipher.update(b"associated_data")

        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()
    except ValueError as e:
        raise ValueError(f"Decryption failed - authentication tag mismatch: {e}")