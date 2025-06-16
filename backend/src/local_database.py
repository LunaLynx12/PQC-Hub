"""
SQLite Database Management Module

This module handles SQLite database initialization, user registration,
message storage, and provides utility functions for database access.

Author: LunaLynx12
"""

import sqlite3
import os
from typing import Optional, Generator
from config import DATABASE


def init_db():
    """
    Initializes the database by creating necessary tables if they don't exist.
    Also creates the database directory if it doesn't exist.
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
    Returns a new connection to the SQLite database.

    @return: SQLite database connection object.
    """
    return sqlite3.connect(DATABASE)


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Dependency for FastAPI to provide a database connection context.

    @yield: SQLite database connection.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def add_user(address: str, dilithium_pub: str, dilithium_priv: str, kyber_pub: str, kyber_priv: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO users (address, dilithium_pub, dilithium_priv, kyber_pub, kyber_priv)
        VALUES (?, ?, ?, ?, ?)
    """, (address, dilithium_pub, dilithium_priv, kyber_pub, kyber_priv))
    conn.commit()
    conn.close()


def get_user_by_address(address: str) -> Optional[dict]:
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