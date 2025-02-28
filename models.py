# models.py
import sqlite3  # Import sqlite3 here
from database import connect_db

# Function to fetch all available rooms
def get_available_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, room_type, price FROM rooms WHERE available = True')
    rooms = cursor.fetchall()
    conn.close()
    return rooms

# Function to book a room
def book_room(user_id, room_id, check_in_date, check_out_date):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Insert booking
        cursor.execute('''
        INSERT INTO bookings (user_id, room_id, check_in_date, check_out_date)
        VALUES (?, ?, ?, ?)
        ''', (user_id, room_id, check_in_date, check_out_date))

        # Mark room as unavailable
        cursor.execute('UPDATE rooms SET available = False WHERE id = ?', (room_id,))

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()