"""
encryption.py

Implements AES-GCM symmetric encryption using shared key from Kyber.
"""

from Crypto.Cipher import AES


def aes_encrypt(key: bytes, plaintext: str) -> bytes:
    cipher = AES.new(key[:32], AES.MODE_GCM)
    cipher.update(b"header")  # Optional but good practice
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return cipher.nonce + tag + ciphertext  # All bytes


def aes_decrypt(key: bytes, data: bytes) -> str:
    """
    Decrypts an AES-GCM encrypted message.

    @param key: Shared key (32 bytes)
    @param data: Encrypted blob: nonce (16B) + ciphertext + tag (16B)
    @return: Decrypted plaintext string
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