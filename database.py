# database.py
import sqlite3
from contextlib import contextmanager

# Function to connect to the database
def connect_db():
    return sqlite3.connect('resort.db')

# Context manager for database connections
@contextmanager
def db_connection():
    """
    Context manager for database connections
    Ensures connections are properly closed even when exceptions occur
    """
    conn = connect_db()
    try:
        yield conn
    finally:
        conn.close()

# Function to initialize the database (create tables)
def init_db():
    with db_connection() as conn:
        cursor = conn.cursor()

        # Create Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
        ''')

        # Create Rooms table (removed available flag)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_type TEXT NOT NULL,
            price REAL NOT NULL,
            capacity INTEGER NOT NULL,
            description TEXT
        )
        ''')

        # Create Bookings table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            check_in_date TEXT NOT NULL,
            check_out_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (room_id) REFERENCES rooms (id)
        )
        ''')

        # Insert sample rooms if they don't exist
        cursor.execute('SELECT COUNT(*) FROM rooms')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
            INSERT INTO rooms (room_type, price, capacity, description)
            VALUES 
                ('Single', 100.0, 1, 'Cozy room with single bed'),
                ('Double', 150.0, 2, 'Comfortable room with queen bed'),
                ('Suite', 250.0, 4, 'Luxurious suite with separate living area')
            ''')

        conn.commit()
        print("Database initialized successfully!")