# validation.py
import re
from datetime import datetime
from database import connect_db

def validate_date_format(date_string):
    """
    Validate that a string is in YYYY-MM-DD format and is a valid date
    Returns True if valid, False otherwise
    """
    # Check format using regex
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
        return False
    
    # Check that it's a valid date
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_room_exists(room_id):
    """
    Validate that a room with the given ID exists in the database
    Returns True if valid, False otherwise
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM rooms WHERE id = ?', (room_id,))
    room = cursor.fetchone()
    conn.close()
    
    return room is not None

def validate_date_order(check_in_date, check_out_date):
    """
    Validate that check_out_date comes after check_in_date
    Returns True if valid, False otherwise
    """
    if not validate_date_format(check_in_date) or not validate_date_format(check_out_date):
        return False
    
    check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
    check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
    
    return check_out > check_in

def validate_room_available(room_id, check_in_date, check_out_date):
    """
    Validate that a room is available for the given date range
    Returns True if available, False otherwise
    """
    if not validate_room_exists(room_id):
        return False
    
    if not validate_date_order(check_in_date, check_out_date):
        return False
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check for overlapping bookings
    cursor.execute('''
        SELECT COUNT(*) FROM bookings 
        WHERE room_id = ? AND 
        (
            (check_in_date <= ? AND check_out_date > ?) OR
            (check_in_date < ? AND check_out_date >= ?) OR
            (check_in_date >= ? AND check_out_date <= ?)
        )
    ''', (room_id, check_out_date, check_in_date, check_out_date, check_in_date, check_in_date, check_out_date))
    
    overlapping_bookings = cursor.fetchone()[0]
    conn.close()
    
    return overlapping_bookings == 0