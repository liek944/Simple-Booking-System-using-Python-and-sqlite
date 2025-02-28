# database.py
import sqlite3

# Function to connect to the database
def connect_db():
    return sqlite3.connect('resort.db')

# Function to initialize the database (create tables)
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    # Create Rooms table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_type TEXT NOT NULL,
        price REAL NOT NULL,
        available BOOLEAN NOT NULL
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
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (room_id) REFERENCES rooms (id)
    )
    ''')

    # Insert sample rooms
    cursor.execute('''
    INSERT OR IGNORE INTO rooms (room_type, price, available)
    VALUES ('Single', 100.0, True),
           ('Double', 150.0, True),
           ('Suite', 250.0, True)
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")