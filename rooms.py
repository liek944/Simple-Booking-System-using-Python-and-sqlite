# rooms.py
from models import get_available_rooms

# Function to display available rooms
def display_rooms():
    rooms = get_available_rooms()
    if rooms:
        print("\nAvailable Rooms:")
        for room in rooms:
            print(f"ID: {room[0]}, Type: {room[1]}, Price: ${room[2]}/night")
    else:
        print("No rooms available.")