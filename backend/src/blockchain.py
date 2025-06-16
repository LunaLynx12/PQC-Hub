"""
Quantum-Resistant Blockchain with Proof-of-Authority

Implements transaction handling, block creation, and simple PoA validation.
Uses Pydantic models consistently for chain structure.

Author: LunaLynx12
"""

from dilithium_py.dilithium import Dilithium2 as Dilithium
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from threading import Lock
import hashlib
import base64
import json


# TODO: check unique registration addresses
# TODO: use validator table from local_database.py
VALIDATORS = ["validator_001", "validator_002"]
BLOCK_TIME_MS = 5000  # Target time between blocks
MAX_TRANSACTIONS_PER_BLOCK = 100


class Transaction(BaseModel):
    """
    Represents a transaction in the blockchain.
    """
    tx_type: str = Field(..., pattern="^(REGISTER|PUBLIC_MESSAGE|GENESIS)$")
    sender: str                                                                     # Wallet address
    receiver: str                                                                   # Can be empty for system-level transactions
    data: Dict[str, str]                                                            # Payload like keys or message hashes

    @field_validator('data')
    @classmethod
    def validate_data(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Data must be a dictionary")
        return {k: str(v) for k, v in v.items()}

class Block(BaseModel):
    """
    Represents a block in the blockchain.
    """
    index: int = Field(..., ge=0)
    validator: str
    transactions: List[Transaction]
    prev_hash: str = Field(..., min_length=64, max_length=64)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    hash: str = ""  # Allow empty initially

    @model_validator(mode='after')
    def compute_hash_after_validation(self) -> 'Block':
        if not self.hash:
            self.hash = self.compute_hash()
        return self

    def compute_hash(self) -> str:
        """Returns SHA-256 hash of the block"""
        block_data = self.model_dump(exclude={"hash"})
        serialized = json.dumps(block_data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(serialized.encode()).hexdigest()
    
class Blockchain:
    """Thread-safe blockchain implementation"""

    def __init__(self):
        self._chain_lock = Lock()
        self._pending_lock = Lock()
        self.chain: List[Block] = [self._create_genesis_block()]
        self.pending_transactions: List[Transaction] = []
    
    def _create_genesis_block(self) -> Block:
        """
        Creates the first block in the chain with proper validation.
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
        """Thread-safe transaction addition"""
        with self._pending_lock:
            if len(self.pending_transactions) >= MAX_TRANSACTIONS_PER_BLOCK:
                return False
            self.pending_transactions.append(tx)
            return True

    def mine_block(self, validator_address: str) -> Optional[Block]:
        """Block creation with validation"""
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
        """Comprehensive block validation"""
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
        """Transaction-specific validation"""
        if tx.tx_type == "REGISTER":
            return self._validate_registration(tx)
        elif tx.tx_type == "PUBLIC_MESSAGE":
            return self._validate_message(tx)
        return True

    def _validate_registration(self, tx: Transaction) -> bool:
        """Validate registration transactions"""
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
        """Chain replacement with validation"""
        with self._chain_lock:
            if self.validate_chain(new_chain) and len(new_chain) > len(self.chain):
                self.chain = new_chain
                return True
            return False

    def validate_chain(self, chain: List[Block]) -> bool:
        """Full chain validation"""
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
    Creates and returns a new transaction.
    """
    return Transaction(
        tx_type=tx_type,
        sender=sender,
        receiver=receiver,
        data=data
    )

_blockchain = Blockchain()

def get_blockchain():
    return _blockchain