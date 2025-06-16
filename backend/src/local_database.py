"""
SQLite Database Management Module

This module handles SQLite database initialization, user registration,
message storage, and provides utility functions for database access.

Author: LunaLynx12
"""


from typing import Optional, Generator
from config import DATABASE
import sqlite3
import os

def init_db():
    """
    Initializes the SQLite database by creating necessary tables if they do not exist.

    - Creates the database directory if it does not already exist.
    - Establishes a connection to the SQLite database file.
    - Creates the following tables:
        - users: Stores user identity and cryptographic keys
        - messages: Stores encrypted messages between users
        - validators: Tracks validator nodes in the network (linked to users)

    return: None
    """
    db_folder = "../database"
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    conn = sqlite3.connect(f"{db_folder}/local_storage.db")
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            address TEXT PRIMARY KEY NOT NULL UNIQUE,
            dilithium_pub TEXT,
            dilithium_priv TEXT,
            kyber_pub TEXT,
            kyber_priv TEXT
        )
    ''')

    # Create messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            content TEXT,
            timestamp TEXT,
            signature TEXT,
            ciphertext TEXT
        )
    ''')

    # Create validator table
    c.execute('''
        CREATE TABLE IF NOT EXISTS validators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL UNIQUE,
            FOREIGN KEY(address) REFERENCES users(address) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


def get_connection() -> sqlite3.Connection:
    """
    Opens and returns a new connection to the SQLite database.

    return: A new SQLite database connection object.
    rtype: sqlite3.Connection
    """
    return sqlite3.connect(DATABASE)


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Provides a FastAPI dependency that yields a database connection context.

    The connection is configured to return rows as dictionaries.
    Ensures proper closing of the connection after use.

    yield: SQLite database connection with dictionary row factory.
    rtype: Generator[sqlite3.Connection, None, None]
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def add_user(address: str, dilithium_pub: str, dilithium_priv: str, kyber_pub: str, kyber_priv: str):
    """
    Adds or updates a user in the database with their cryptographic key material.

    Uses an 'INSERT OR REPLACE' statement to ensure idempotency.

    param address: User's unique wallet address (primary key)
    type address: str
    param dilithium_pub: Dilithium public key
    type dilithium_pub: str
    param dilithium_priv: Dilithium private key
    type dilithium_priv: str
    param kyber_pub: Kyber public key
    type kyber_pub: str
    param kyber_priv: Kyber private key
    type kyber_priv: str
    return: None
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO users (address, dilithium_pub, dilithium_priv, kyber_pub, kyber_priv)
        VALUES (?, ?, ?, ?, ?)
    """, (address, dilithium_pub, dilithium_priv, kyber_pub, kyber_priv))
    conn.commit()
    conn.close()


def get_user_by_address(address: str) -> Optional[dict]:
    """
    Retrieves a user's public and private key information based on their address.

    Returns the data as a dictionary if found, otherwise returns None.

    param address: Wallet address of the user to look up
    type address: str
    return: Dictionary containing user key data, or None if not found
    rtype: Optional[dict]
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dilithium_pub, dilithium_priv, kyber_pub FROM users WHERE address = ?", (address,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            "address" : address,
            "dilithium_pub": result[0],
            "dilithium_priv" : result[1],
            "kyber_pub": result[2]
        }
    return None