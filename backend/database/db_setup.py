# backend/database/db_setup.py
import sqlite3

def create_connection():
    conn = sqlite3.connect('rules.db')
    return conn

def setup_database():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create a table for storing rules
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
