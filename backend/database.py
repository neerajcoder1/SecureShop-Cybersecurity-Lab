import sqlite3
import os
import logging
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'secure_shop.db')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')

    # Products Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0
        )
    ''')

    # Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    # Reviews Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    # Insert dummy products if none exist
    cursor.execute("SELECT COUNT(*) as count FROM products")
    if cursor.fetchone()['count'] == 0:
        dummy_products = [
            ("Secure Laptop", "A laptop with hardware security features.", 1299.99, 10),
            ("Encrypted Drive", "1TB hardware-encrypted USB drive.", 150.00, 50),
            ("Privacy Screen", "Screen filter to prevent shoulder surfing.", 35.00, 100)
        ]
        # SECURE: Parameterized Query used for insertion
        cursor.executemany(
            "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
            dummy_products
        )
        logger.info("Inserted dummy products.")

    conn.commit()
    conn.close()

# --- SECURE QUERY EXECUTION HELPERS ---
# We use standard ? parameterization for all SQL operations to prevent SQL Injection

def execute_read_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Executes a SELECT query securely using parameters."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # SECURE: params tuple is passed to execute()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return []
    finally:
        conn.close()

def execute_write_query(query: str, params: tuple = ()) -> Optional[int]:
    """Executes an INSERT/UPDATE/DELETE query securely using parameters."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # SECURE: params tuple is passed to execute()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
    finally:
        conn.close()
