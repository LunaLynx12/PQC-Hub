"""
Global configuration constants used across the application.
Includes database path, cryptographic keys, peer network settings, and blockchain parameters.

Author: LunaLynx12
"""


DATABASE = "../database/local_storage.db"
"""
Path to the SQLite database file used for local storage.

This path is relative to the project root directory.
"""

TEST_KEY = b'i\xc1\xf2!\r\xaf\x14\x0fs\xcfQ@\xb5VB\xe87q\x8b\xa4\xaatU\xe8\xcc\x94\x9b\x17\x07\xe3^\xff'
"""
Predefined test cryptographic key used for development and testing purposes.

This is a raw bytes value intended for symmetric encryption/decryption.
"""

KNOWN_PEERS = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
    "http://localhost:8004",
    "http://localhost:8005",
    "http://localhost:8006",
    "http://localhost:8007",
    "http://localhost:8008",
    "http://localhost:8009"
]
"""
List of known peer node URLs in the P2P network.

These are used for discovery and initial connection during startup.
Each URL points to another instance of the FastAPI service running on a different port.
"""

VALIDATORS = ["validator_001", "validator_002"]
"""
List of trusted validator identifiers currently active in the network.

Used for testing consensus and validation logic.
"""

MAX_TRANSACTIONS_PER_BLOCK = 100
"""
Maximum number of transactions allowed in a single block.

Imposes a limit to prevent oversized blocks and ensure system stability.
"""