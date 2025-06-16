"""
Quantum-Resistant Blockchain with Proof-of-Authority

Implements transaction handling, block creation, and simple PoA validation.
Uses Pydantic models consistently for chain structure.

Author: LunaLynx12
"""

# TODO: check unique registration addresses
# TODO: use validator table from local_database.py

from pydantic import BaseModel, Field, field_validator, model_validator
from dilithium_py.dilithium import Dilithium2 as Dilithium
from config import VALIDATORS, MAX_TRANSACTIONS_PER_BLOCK
from typing import List, Dict, Optional
from datetime import datetime
from threading import Lock
import hashlib
import base64
import json


class Transaction(BaseModel):
    """
    Represents a single transaction in the blockchain.

    Attributes:
        tx_type (str): Type of transaction - must be one of: REGISTER, PUBLIC_MESSAGE, GENESIS
        sender (str): Wallet address of the sender
        receiver (str): Wallet address of the recipient (can be empty for system-level transactions)
        data (Dict[str, str]): Payload data such as keys or message hashes
    """
    tx_type: str = Field(..., pattern="^(REGISTER|PUBLIC_MESSAGE|GENESIS)$")
    sender: str                                                                     # Wallet address
    receiver: str                                                                   # Can be empty for system-level transactions
    data: Dict[str, str]                                                            # Payload like keys or message hashes

    @field_validator('data')
    @classmethod
    def validate_data(cls, v):
        """
        Validates that the `data` field is a dictionary and ensures all values are strings.

        param v: The value to validate
        type v: dict
        return: Sanitized dictionary with string values
        raises ValueError: If input is not a dictionary or contains non-string values
        """
        if not isinstance(v, dict):
            raise ValueError("Data must be a dictionary")
        return {k: str(v) for k, v in v.items()}

class Block(BaseModel):
    """
    Represents a single block in the blockchain.

    Attributes:
        index (int): Position in the blockchain (non-negative integer)
        validator (str): Address of the validator who mined this block
        transactions (List[Transaction]): List of transactions included in the block
        prev_hash (str): SHA-256 hash of the previous block (exactly 64 characters)
        timestamp (str): UTC timestamp when block was created (ISO format)
        hash (str): SHA-256 hash of the block contents (computed automatically)
    """
    index: int = Field(..., ge=0)
    validator: str
    transactions: List[Transaction]
    prev_hash: str = Field(..., min_length=64, max_length=64)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    hash: str = ""                                                                  # Allow empty initially

    @model_validator(mode='after')
    def compute_hash_after_validation(self) -> 'Block':
        """
        Automatically computes and sets the block hash if it's empty.

        return: Updated Block instance with computed hash
        """
        if not self.hash:
            self.hash = self.compute_hash()
        return self

    def compute_hash(self) -> str:
        """
        Computes and returns the SHA-256 hash of the block.

        return: Hex-encoded SHA-256 hash string
        """
        block_data = self.model_dump(exclude={"hash"})
        serialized = json.dumps(block_data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(serialized.encode()).hexdigest()
    
class Blockchain:
    """
    Thread-safe implementation of a blockchain with Proof-of-Authority consensus.

    Features:
        - Transaction pooling
        - Block mining
        - Chain validation
        - Secure signing/verification using Dilithium
    """
    def __init__(self):
        """
        Initializes a new blockchain instance with:
            - Genesis block
            - Empty pending transaction pool
            - Thread locks for safe concurrent access
        """
        self._chain_lock = Lock()
        self._pending_lock = Lock()
        self.chain: List[Block] = [self._create_genesis_block()]
        self.pending_transactions: List[Transaction] = []
    
    def _create_genesis_block(self) -> Block:
        """
        Creates the first block in the blockchain with proper validation.

        return: Genesis block instance
        """
        # Create genesis transaction
        genesis_tx = Transaction(
            tx_type="GENESIS",
            sender="0",
            receiver="",
            data={"name": "Genesis Block"}
        )

        # Create block without hash (bypass Pydantic validation)
        genesis_block = Block.model_construct(
            index=0,
            validator="system",
            transactions=[genesis_tx],
            prev_hash="0" * 64,
            timestamp=datetime.utcnow().isoformat(),
            hash=""
        )

        # Compute and set the hash
        genesis_block.hash = genesis_block.compute_hash()

        return genesis_block

    def add_transaction(self, tx: Transaction) -> bool:
        """
        Adds a transaction to the pending pool in a thread-safe manner.

        param tx: Transaction to add
        type tx: Transaction
        return: True if added successfully, False if pool is full
        """
        with self._pending_lock:
            if len(self.pending_transactions) >= MAX_TRANSACTIONS_PER_BLOCK:
                return False
            self.pending_transactions.append(tx)
            return True

    def mine_block(self, validator_address: str) -> Optional[Block]:
        """
        Mines a new block from pending transactions by a valid validator.

        param validator_address: Address of the validator attempting to mine
        type validator_address: str
        return: New mined block if successful, None otherwise
        """
        print(f"[DEBUG] Attempting to mine block by {validator_address}")

        if validator_address not in VALIDATORS:
            print(f"[ERROR] Validator {validator_address} not authorized")
            return None

        with self._chain_lock, self._pending_lock:
            if not self.pending_transactions:
                print("[WARNING] No pending transactions to mine")
                return None

            print(f"[INFO] Mining block with {len(self.pending_transactions)} transactions")

            last_block = self.chain[-1]
            new_block = Block(
                index=last_block.index + 1,
                validator=validator_address,
                transactions=self.pending_transactions.copy(),
                prev_hash=last_block.hash,
            )
            new_block.hash = new_block.compute_hash()

            print(f"[DEBUG] New block computed hash: {new_block.hash}")

            if self.validate_block(new_block):
                print("[SUCCESS] Block validated successfully")
                self.pending_transactions.clear()
                self.chain.append(new_block)
                return new_block
            else:
                print("[ERROR] Block failed validation")
                return None

    def validate_block(self, block: Block) -> bool:
        """
        Performs comprehensive validation of a block before adding to the chain.

        param block: Block to validate
        type block: Block
        return: True if block is valid, False otherwise
        """
        # Basic structural checks
        if not block.hash == block.compute_hash():
            return False

        # Transaction validation
        for tx in block.transactions:
            if not self._validate_transaction(tx):
                return False

        # Chain continuity check
        if block.index > 0:
            prev_block = self.chain[block.index - 1]
            if block.prev_hash != prev_block.hash:
                return False

        return True

    def _validate_transaction(self, tx: Transaction) -> bool:
        """
        Validates individual transactions based on type.

        param tx: Transaction to validate
        type tx: Transaction
        return: True if transaction is valid, False otherwise
        """
        if tx.tx_type == "REGISTER":
            return self._validate_registration(tx)
        elif tx.tx_type == "PUBLIC_MESSAGE":
            return self._validate_message(tx)
        return True

    def _validate_registration(self, tx: Transaction) -> bool:
        """
        Validates registration transactions with digital signature.

        param tx: Registration transaction to validate
        type tx: Transaction
        return: True if signature is valid, False otherwise
        """
        required_fields = {"dilithium_pub", "kyber_pub", "signature"}
        if not required_fields.issubset(tx.data.keys()):
            return False

        try:
            pub_key = base64.b64decode(tx.data["dilithium_pub"])
            signature = base64.b64decode(tx.data["signature"])
            message = f"REGISTER:{tx.sender}"
            return Dilithium.verify(pub_key, message.encode(), signature)
        except:
            return False

    def _validate_message(self, tx: Transaction) -> bool:
        """
        Validates public message transactions with digital signature.

        param tx: Message transaction to validate
        type tx: Transaction
        return: True if signature is valid, False otherwise
        """
        print(f"[DEBUG] Validating PUBLIC_MESSAGE: {tx.data.keys()}")
        if "message_hash" not in tx.data:
            print("[ERROR] Missing 'message_hash'")
            return False
        if "signature" not in tx.data:
            print("[ERROR] Missing 'signature'")
            return False
        if "dilithium_pub" not in tx.data:
            print("[ERROR] Missing 'dilithium_pub'")
            return False

        try:
            pub_key = base64.b64decode(tx.data["dilithium_pub"])
            signature = base64.b64decode(tx.data["signature"])
            return Dilithium.verify(pub_key, tx.data["message_hash"].encode(), signature)
        except Exception as e:
            print(f"[ERROR] Signature verification failed: {str(e)}")
            return False

    def replace_chain(self, new_chain: List[Block]) -> bool:
        """
        Replaces the current chain with a longer, valid incoming chain.

        param new_chain: Candidate chain to replace current chain
        type new_chain: List[Block]
        return: True if chain replaced, False otherwise
        """
        with self._chain_lock:
            if self.validate_chain(new_chain) and len(new_chain) > len(self.chain):
                self.chain = new_chain
                return True
            return False

    def validate_chain(self, chain: List[Block]) -> bool:
        """
        Validates an entire blockchain chain for consistency and integrity.

        param chain: Chain to validate
        type chain: List[Block]
        return: True if chain is valid, False otherwise
        """
        if not chain or chain[0].index != 0:
            return False

        for i in range(1, len(chain)):
            if not self.validate_block(chain[i]):
                return False
            if chain[i].prev_hash != chain[i-1].hash:
                return False

        return True

def create_transaction(tx_type: str, sender: str, receiver: str, data: dict) -> Transaction:
    """
    Factory function to create and return a new transaction.

    param tx_type: Type of transaction (REGISTER, PUBLIC_MESSAGE, GENESIS)
    type tx_type: str
    param sender: Sender wallet address
    type sender: str
    param receiver: Receiver wallet address
    type receiver: str
    param data: Dictionary containing transaction payload
    type data: dict
    return: Newly created Transaction object
    """
    return Transaction(
        tx_type=tx_type,
        sender=sender,
        receiver=receiver,
        data=data
    )

_blockchain = Blockchain()
"""
Singleton instance of the blockchain shared across the application.
"""

def get_blockchain():
    """
    Returns the singleton instance of the blockchain.

    return: Shared Blockchain instance
    rtype: Blockchain
    """
    return _blockchain