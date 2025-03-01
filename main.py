# main.py
from auth import register_user, login_user
from rooms import display_rooms
from bookings import book_room_ui, display_user_bookings, cancel_booking_ui, modify_booking_ui
from database import init_db

# Initialize the database
init_db()

# Main menu
def main():
    while True:
        print("\n" + "=" * 50)
        print("Welcome to the Resort Booking System!")
        print("=" * 50)
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("-" * 50)
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            email = input("Enter your email (optional): ")
            phone = input("Enter your phone number (optional): ")
            
            if register_user(username, password, email, phone):
                print("Registration successful!")
            else:
                print("Username already exists. Please try again.")
                
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_id = login_user(username, password)
            
            if user_id:
                print(f"Login successful! Welcome back, {username}!")
                user_menu(user_id)
            else:
                print("Invalid username or password.")
                
        elif choice == '3':
            print("Thank you for using the Resort Booking System. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

# User menu after login
def user_menu(user_id):
    while True:
        print("\n" + "=" * 50)
        print("User Menu")
        print("=" * 50)
        print("1. View Available Rooms")
        print("2. Book a Room")
        print("3. View My Bookings")
        print("4. Cancel a Booking")
        print("5. Modify a Booking")
        print("6. Logout")
        print("-" * 50)
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            display_rooms()
        elif choice == '2':
            book_room_ui(user_id)
        elif choice == '3':
            display_user_bookings(user_id)
        elif choice == '4':
            cancel_booking_ui(user_id)
        elif choice == '5':
            modify_booking_ui(user_id)
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == '__main__':
    main()