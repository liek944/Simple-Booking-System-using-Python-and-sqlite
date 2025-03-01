# models.py
from database import db_connection
from validation import validate_room_available
from datetime import datetime

# Function to fetch all available rooms for a specific date range
def get_available_rooms(check_in_date, check_out_date):
    with db_connection() as conn:
        cursor = conn.cursor()
        
        # Get all rooms
        cursor.execute('SELECT id, room_type, price, capacity, description FROM rooms')
        all_rooms = cursor.fetchall()
        
        # Filter out rooms that have overlapping bookings
        available_rooms = []
        for room in all_rooms:
            room_id = room[0]
            
            # Check for overlapping bookings
            cursor.execute('''
                SELECT COUNT(*) FROM bookings 
                WHERE room_id = ? AND status = 'confirmed' AND
                (
                    (check_in_date <= ? AND check_out_date > ?) OR
                    (check_in_date < ? AND check_out_date >= ?) OR
                    (check_in_date >= ? AND check_out_date <= ?)
                )
            ''', (room_id, check_out_date, check_in_date, check_out_date, check_in_date, check_in_date, check_out_date))
            
            overlapping_bookings = cursor.fetchone()[0]
            
            if overlapping_bookings == 0:
                available_rooms.append(room)
        
        return available_rooms

# Function to book a room
def book_room(user_id, room_id, check_in_date, check_out_date):
    if not validate_room_available(room_id, check_in_date, check_out_date):
        return False
    
    with db_connection() as conn:
        cursor = conn.cursor()
        
        try:
            # Insert booking
            cursor.execute('''
            INSERT INTO bookings (user_id, room_id, check_in_date, check_out_date, status, created_at)
            VALUES (?, ?, ?, ?, 'confirmed', CURRENT_TIMESTAMP)
            ''', (user_id, room_id, check_in_date, check_out_date))
            
            conn.commit()
            return cursor.lastrowid  # Return the booking ID
        except Exception as e:
            print(f"Error booking room: {e}")
            conn.rollback()
            return False

# Function to get a user's bookings
def get_user_bookings(user_id):
    with db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.id, r.room_type, r.price, b.check_in_date, b.check_out_date, b.status
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.user_id = ?
            ORDER BY b.check_in_date
        ''', (user_id,))
        
        return cursor.fetchall()

# Function to cancel a booking
def cancel_booking(booking_id, user_id):
    with db_connection() as conn:
        cursor = conn.cursor()
        
        # Verify the booking belongs to the user
        cursor.execute('SELECT id FROM bookings WHERE id = ? AND user_id = ?', (booking_id, user_id))
        if not cursor.fetchone():
            return False
        
        try:
            cursor.execute('UPDATE bookings SET status = "cancelled" WHERE id = ?', (booking_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error cancelling booking: {e}")
            conn.rollback()
            return False

# Function to modify a booking
def modify_booking(booking_id, user_id, new_check_in_date, new_check_out_date):
    with db_connection() as conn:
        cursor = conn.cursor()
        
        # Verify the booking belongs to the user
        cursor.execute('SELECT room_id FROM bookings WHERE id = ? AND user_id = ?', (booking_id, user_id))
        result = cursor.fetchone()
        if not result:
            return False
        
        room_id = result[0]
        
        # Check if the room is available for the new dates (excluding this booking)
        cursor.execute('''
            SELECT COUNT(*) FROM bookings 
            WHERE room_id = ? AND id != ? AND status = 'confirmed' AND
            (
                (check_in_date <= ? AND check_out_date > ?) OR
                (check_in_date < ? AND check_out_date >= ?) OR
                (check_in_date >= ? AND check_out_date <= ?)
            )
        ''', (room_id, booking_id, new_check_out_date, new_check_in_date, new_check_out_date, new_check_in_date, new_check_in_date, new_check_out_date))
        
        if cursor.fetchone()[0] > 0:
            return False  # Room not available for new dates
        
        try:
            cursor.execute('''
                UPDATE bookings 
                SET check_in_date = ?, check_out_date = ? 
                WHERE id = ?
            ''', (new_check_in_date, new_check_out_date, booking_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error modifying booking: {e}")
            conn.rollback()
            return False