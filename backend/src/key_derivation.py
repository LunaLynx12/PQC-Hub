"""
Instead of randomly generating keys each time, use the mnemonic as a seed to deterministically derive cryptographic keys.

Author: LunaLynx12
"""


from dilithium_py.dilithium import Dilithium2 as Dilithium
from mnemonics import seed_to_master_key
from kyber_py.ml_kem import ML_KEM_512
from typing import Tuple


def derive_dilithium_keypair(mnemonic: str) -> Tuple[bytes, bytes]:
    """
    Deterministically derives Dilithium keypair from mnemonic.

    :param mnemonic: Recovery phrase (12–24 words)
    :return: (public_key, secret_key) bytes
    """
    seed = seed_to_master_key(mnemonic)
    return Dilithium.keygen(seed[:32])  # Use first 32 bytes as seed


def derive_kyber_keypair(mnemonic: str) -> Tuple[bytes, bytes]:
    """
    Deterministically derives Kyber keypair from mnemonic.

    :param mnemonic: Recovery phrase (12–24 words)
    :return: (public_key, secret_key) bytes
    """
    seed = seed_to_master_key(mnemonic)
    return generate_kyber_keys_from_seed(seed)


def generate_kyber_keys_from_seed(seed: bytes) -> Tuple[bytes, bytes]:
    """
    Custom Kyber key generation using deterministic seed.

    :param seed: Random entropy used to derive keys
    :return: (public_key, secret_key) bytes
    """
    # You can hash or split the seed further if needed
    public_key, secret_key = ML_KEM_512.keygen(seed[:32])
    return public_key, secret_key