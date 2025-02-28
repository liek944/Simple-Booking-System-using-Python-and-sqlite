# main.py
from auth import register_user, login_user
from rooms import display_rooms
from bookings import book_room_ui
from database import init_db

# Initialize the database
init_db()

# Main menu
def main():
    while True:
        print("\nWelcome to the Resort Booking System!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            if register_user(username, password):
                print("Registration successful!")
            else:
                print("Username already exists. Please try again.")
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_id = login_user(username, password)
            if user_id:
                print("Login successful!")
                while True:
                    print("\n1. View Available Rooms")
                    print("2. Book a Room")
                    print("3. Logout")
                    user_choice = input("Choose an option: ")

                    if user_choice == '1':
                        display_rooms()
                    elif user_choice == '2':
                        book_room_ui(user_id)
                    elif user_choice == '3':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == '__main__':
    main()