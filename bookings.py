# bookings.py
from models import book_room, get_user_bookings, cancel_booking, modify_booking
from validation import validate_date_format, validate_room_exists, validate_date_order, validate_room_available

# Function to book a room with validation
def book_room_ui(user_id):
    room_id = input("Enter the room ID you want to book: ")
    check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
    
    # Validate inputs
    if not room_id.isdigit():
        print("Error: Room ID must be a number.")
        return
    
    if not validate_date_format(check_in_date):
        print("Error: Check-in date must be in YYYY-MM-DD format.")
        return
    
    if not validate_date_format(check_out_date):
        print("Error: Check-out date must be in YYYY-MM-DD format.")
        return
    
    if not validate_date_order(check_in_date, check_out_date):
        print("Error: Check-out date must be after check-in date.")
        return
    
    if not validate_room_exists(room_id):
        print("Error: Room does not exist.")
        return
    
    if not validate_room_available(room_id, check_in_date, check_out_date):
        print("Error: Room is not available for the selected dates.")
        return
    
    # Book the room
    booking_id = book_room(user_id, room_id, check_in_date, check_out_date)
    if booking_id:
        print(f"Booking successful! Your booking ID is: {booking_id}")
    else:
        print("Booking failed. Please try again.")

# Function to display user's bookings
def display_user_bookings(user_id):
    bookings = get_user_bookings(user_id)
    
    if not bookings:
        print("You have no bookings.")
        return
    
    print("\nYour Bookings:")
    print("-" * 80)
    print(f"{'ID':<5} {'Room Type':<15} {'Price':<10} {'Check-in':<12} {'Check-out':<12} {'Status':<10}")
    print("-" * 80)
    
    for booking in bookings:
        booking_id, room_type, price, check_in, check_out, status = booking
        print(f"{booking_id:<5} {room_type:<15} ${price:<9.2f} {check_in:<12} {check_out:<12} {status:<10}")

# Function to cancel a booking
def cancel_booking_ui(user_id):
    display_user_bookings(user_id)
    
    booking_id = input("\nEnter the ID of the booking you want to cancel (or 0 to go back): ")
    
    if booking_id == '0':
        return
    
    if not booking_id.isdigit():
        print("Error: Booking ID must be a number.")
        return
    
    if cancel_booking(int(booking_id), user_id):
        print("Booking cancelled successfully!")
    else:
        print("Failed to cancel booking. Please try again.")

# Function to modify a booking
def modify_booking_ui(user_id):
    display_user_bookings(user_id)
    
    booking_id = input("\nEnter the ID of the booking you want to modify (or 0 to go back): ")
    
    if booking_id == '0':
        return
    
    if not booking_id.isdigit():
        print("Error: Booking ID must be a number.")
        return
    
    check_in_date = input("Enter new check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter new check-out date (YYYY-MM-DD): ")
    
    # Validate inputs
    if not validate_date_format(check_in_date):
        print("Error: Check-in date must be in YYYY-MM-DD format.")
        return
    
    if not validate_date_format(check_out_date):
        print("Error: Check-out date must be in YYYY-MM-DD format.")
        return
    
    if not validate_date_order(check_in_date, check_out_date):
        print("Error: Check-out date must be after check-in date.")
        return
    
    if modify_booking(int(booking_id), user_id, check_in_date, check_out_date):
        print("Booking modified successfully!")
    else:
        print("Failed to modify booking. Please check if the room is available for the new dates.")