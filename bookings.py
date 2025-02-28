# bookings.py
from models import book_room

# Function to book a room
def book_room_ui(user_id):
    room_id = input("Enter the room ID you want to book: ")
    check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter check-out date (YYYY-MM-DD): ")

    if book_room(user_id, room_id, check_in_date, check_out_date):
        print("Booking successful!")
    else:
        print("Booking failed. Please try again.")