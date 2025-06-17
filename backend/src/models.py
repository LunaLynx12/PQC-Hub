"""
Data Models Module

This module defines Pydantic models used throughout the application,
including User, Message, and Registration request structures.

Author: LunaLynx12
"""

from pydantic import BaseModel, Field

class User(BaseModel):
    """
    Represents a registered user in the system.
    """
    address: str
    dilithium_pub: str
    kyber_pub: str

class Message(BaseModel):
    """
    Represents a message exchanged between users.
    Set receiver to 'public' for public messages (stored on-chain).
    """
    id: int = Field(default="", description="Auto-filled by server")
    sender: str
    receiver: str = "public"
    content: str
    timestamp: str = Field(default="", description="Auto-filled by server")
    signature: str = Field(default="", description="Auto-filled by server")
    ciphertext: str = Field(default="", description="Auto-filled by server")

class UserRegisterRequest(BaseModel):
    """
    Model for incoming user registration requests.
    """
    #address: str = "0x1234567890"
    pass

class EncryptedMessage(BaseModel):
    sender: str
    receiver: str
    content: str  # This will be the encrypted blob
    timestamp: str = Field(default="", description="Auto-filled by server")
    ciphertext: str  # Optional if storing separately