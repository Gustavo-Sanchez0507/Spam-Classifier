import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_conn():
    """Get a new database connection. Returns None if DATABASE_URL not configured."""
    if not DATABASE_URL:
        return None
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Initialize database by creating required tables if they don't exist."""
    conn = get_db_conn()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        message TEXT NOT NULL,
        prediction VARCHAR(20) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_message(message, prediction):
    """Insert a new message and its prediction into the database.
    Returns True if successful, False if database is not available."""
    conn = get_db_conn()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO messages (message, prediction) VALUES (%s, %s)', 
                   (message, prediction))
        conn.commit()
        success = True
    except Exception:
        conn.rollback()
        success = False
    finally:
        cur.close()
        conn.close()
    return success

def get_history(limit=20):
    """Get the most recent messages from the database.
    Returns empty list if database is not available."""
    conn = get_db_conn()
    if not conn:
        return []
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('''
            SELECT id, message, prediction, created_at 
            FROM messages 
            ORDER BY id DESC 
            LIMIT %s
        ''', (limit,))
        rows = cur.fetchall()
    except Exception:
        rows = []
    finally:
        cur.close()
        conn.close()
    return rows

def delete_message(message_id):
    """Delete a message from the database by its ID.
    Returns True if successful, False if database is not available or deletion fails."""
    conn = get_db_conn()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM messages WHERE id = %s', (message_id,))
        conn.commit()
        success = True
    except Exception:
        conn.rollback()
        success = False
    finally:
        cur.close()
        conn.close()
    return success

# Initialize the database tables when this module is imported
try:
    init_db()
except Exception as e:
    print(f"Warning: Could not initialize database: {e}")