"""
kyber.py

Implements post-quantum key encapsulation using ML-KEM 512.
Used to derive shared secrets for symmetric encryption (e.g., AES).

Author: LunaLynx12
"""

from kyber_py.ml_kem import ML_KEM_512


def generate_kyber_keys():
    """
    Generates a Kyber public/secret keypair.

    @return: Tuple of (public_key_bytes, secret_key_bytes)
    """
    public_key, secret_key = ML_KEM_512.keygen()
    return public_key, secret_key


def generate_shared_key(public_key: bytes) -> tuple[bytes, bytes]:
    """
    Sender uses recipient's public key to generate shared key + ciphertext.

    @param public_key: Recipient's Kyber public key.
    @return: (shared_key, ciphertext)
    """
    return ML_KEM_512.encaps(public_key)


def recover_shared_key(secret_key: bytes, ciphertext: bytes) -> bytes:
    """
    Receiver uses their secret key to recover the shared key.

    @param secret_key: Recipient's Kyber secret key.
    @param ciphertext: Data sent by sender.
    @return: Shared secret key.
    """
    return ML_KEM_512.decaps(secret_key, ciphertext)