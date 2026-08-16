import sqlite3
import os
import logging
from typing import List, Dict, Any, Optional

# Project root:
# /opt/render/project/src
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SQLite database:
# /opt/render/project/src/database/secure_shop.db
DB_PATH = os.path.join(BASE_DIR, "database", "secure_shop.db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Make sure the database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

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

    # Phase 3: User Challenges Table Migration
    # Check if lab_id exists in user_challenges to perform safe migration
    cursor.execute("PRAGMA table_info(user_challenges)")
    columns = [col['name'] for col in cursor.fetchall()]
    
    if 'lab_id' not in columns and len(columns) > 0:
        logger.info("Migrating user_challenges to Phase 3 schema...")
        cursor.execute("ALTER TABLE user_challenges RENAME TO user_challenges_old")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lab_id TEXT NOT NULL,
                challenge_id INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                xp_awarded INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id),
                UNIQUE(user_id, lab_id, challenge_id)
            )
        ''')
        
        cursor.execute('''
            INSERT INTO user_challenges (id, user_id, lab_id, challenge_id, completed_at, xp_awarded)
            SELECT id, user_id, 'secureshop', challenge_id, completed_at, 50 FROM user_challenges_old
        ''')
        cursor.execute("DROP TABLE user_challenges_old")
    else:
        # Create standard table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lab_id TEXT NOT NULL,
                challenge_id INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                xp_awarded INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id),
                UNIQUE(user_id, lab_id, challenge_id)
            )
        ''')

    # Insert dummy products if none exist
    cursor.execute("SELECT COUNT(*) as count FROM products")

    if cursor.fetchone()['count'] == 0:
        dummy_products = [
            (
                "Secure Laptop",
                "A laptop with hardware security features.",
                1299.99,
                10
            ),
            (
                "Encrypted Drive",
                "1TB hardware-encrypted USB drive.",
                150.00,
                50
            ),
            (
                "Privacy Screen",
                "Screen filter to prevent shoulder surfing.",
                35.00,
                100
            )
        ]

        cursor.executemany(
            "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
            dummy_products
        )

        logger.info("Inserted dummy products.")

    conn.commit()
    conn.close()


# --- SECURE QUERY EXECUTION HELPERS ---

def execute_read_query(
    query: str,
    params: tuple = ()
) -> List[Dict[str, Any]]:
    """Executes a SELECT query securely using parameters."""

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return []

    finally:
        conn.close()


def execute_write_query(
    query: str,
    params: tuple = ()
) -> Optional[int]:
    """Executes an INSERT/UPDATE/DELETE query securely using parameters."""

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None

    finally:
        conn.close()