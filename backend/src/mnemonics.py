import os
import hashlib
from typing import List
from config import WORDLIST

def generate_entropy(num_bits: int = 160) -> bytes:
    """
    Generate secure entropy of specified bit-length.
    
    :param num_bits: Bit length of entropy (must be divisible by 32 and ≥ 128)
    :return: Entropy as bytes
    :raises ValueError: If invalid bit length
    """
    if num_bits < 128 or num_bits > 256 or num_bits % 32 != 0:
        raise ValueError("Invalid bit length")
    return os.urandom(num_bits // 8)


def entropy_to_mnemonic(entropy: bytes) -> List[str]:
    """
    Convert entropy to a mnemonic phrase using BIP-39 word list.
    
    :param entropy: Entropy bytes
    :return: List of mnemonic words
    :raises ValueError: If WORDLIST is not valid size
    """
    if len(WORDLIST) != 2048:
        raise ValueError(f"WORDLIST must contain exactly 2048 words, got {len(WORDLIST)}")

    entropy_int = int.from_bytes(entropy, byteorder="big")
    entropy_bits = len(entropy) * 8
    checksum_bits = entropy_bits // 32

    # Calculate and append checksum
    h = hashlib.sha256(entropy).digest()
    checksum = int.from_bytes(h, byteorder="big") >> (256 - checksum_bits)

    combined = (entropy_int << checksum_bits) | checksum
    total_bits = entropy_bits + checksum_bits

    # Split into 11-bit chunks and map to WORDLIST
    chunks = [
        WORDLIST[(combined >> (total_bits - 11 * (i + 1))) & 0x7FF]
        for i in range(total_bits // 11)
    ]

    return chunks


def generate_mnemonic_phrase(word_count: int = 12) -> str:
    """
    Generate a mnemonic phrase with a specific number of words.
    
    :param word_count: Number of words (12, 15, 18, 21, 24)
    :return: Mnemonic string
    :raises ValueError: If unsupported word count
    """
    bits_map = {
        12: 128,
        15: 160,
        18: 192,
        21: 224,
        24: 256,
    }
    if word_count not in bits_map:
        raise ValueError(f"Word count must be one of {list(bits_map.keys())}")

    entropy = generate_entropy(bits_map[word_count])
    return " ".join(entropy_to_mnemonic(entropy))

def seed_to_master_key(mnemonic: str, passphrase: str = "") -> bytes:
    """
    Convert mnemonic + passphrase to a 64-byte seed.
    """
    salt = "mnemonic" + passphrase
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode(), salt.encode(), 2048, dklen=64)