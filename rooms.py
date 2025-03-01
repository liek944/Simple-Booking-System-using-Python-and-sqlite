# rooms.py
from models import get_available_rooms
from validation import validate_date_format, validate_date_order

# Function to display available rooms for a date range
def display_rooms():
    print("\nSearch for Available Rooms")
    print("--------------------------")
    
    check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
    
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
    
    rooms = get_available_rooms(check_in_date, check_out_date)
    
    if rooms:
        print(f"\nAvailable Rooms for {check_in_date} to {check_out_date}:")
        print("-" * 80)
        print(f"{'ID':<5} {'Type':<15} {'Price':<10} {'Capacity':<10} {'Description':<40}")
        print("-" * 80)
        
        for room in rooms:
            room_id, room_type, price, capacity, description = room
            print(f"{room_id:<5} {room_type:<15} ${price:<9.2f} {capacity:<10} {description[:40]}")
    else:
        print("No rooms available for the selected dates.")