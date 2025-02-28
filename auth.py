# auth.py
import sqlite3  # Import sqlite3 here
from database import connect_db

# Function to register a new user
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Function to log in a user
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return user[0]  # Return the user ID
    else:
        return None