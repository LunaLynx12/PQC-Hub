"""
Implements post-quantum key encapsulation using ML-KEM 512.
Used to derive shared secrets for symmetric encryption (AES-GCM).

Author: LunaLynx12
"""


from kyber_py.ml_kem import ML_KEM_512

def generate_kyber_keys():
    """
    Generates a Kyber public/secret keypair using ML-KEM 512.

    return: Tuple containing:
        - public_key (bytes): Encoded public key for sharing
        - secret_key (bytes): Secret key for decryption
    """
    public_key, secret_key = ML_KEM_512.keygen()
    return public_key, secret_key


def generate_shared_key(public_key: bytes) -> tuple[bytes, bytes]:
    """
    Generates a shared secret key and its associated ciphertext.

    This function is typically used by the sender who has the recipient's public key.

    param public_key: The recipient's Kyber public key as bytes.
    type public_key: bytes
    return: Tuple containing:
        - shared_key (bytes): Symmetric key derived during encapsulation
        - ciphertext (bytes): Encrypted data to be sent to the recipient
    """
    return ML_KEM_512.encaps(public_key)


def recover_shared_key(secret_key: bytes, ciphertext: bytes) -> bytes:
    """
    Recovers the shared secret key using the recipient's secret key and ciphertext.

    This function is typically used by the receiver to extract the shared key.

    param secret_key: Recipient's private Kyber key.
    type secret_key: bytes
    param ciphertext: Encapsulated data received from the sender.
    type ciphertext: bytes
    return: Shared secret key used for symmetric encryption/decryption.
    rtype: bytes
    """
    return ML_KEM_512.decaps(secret_key, ciphertext)