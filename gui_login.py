# resort_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # You might need to install this with: pip install tkcalendar
import datetime

from auth import login_user, register_user
from models import get_available_rooms, book_room, get_user_bookings, cancel_booking, modify_booking
from database import init_db
from validation import validate_date_order, validate_room_available

class ResortBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resort Booking System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.user_id = None
        self.username = None
        
        # Initialize database
        init_db()
        
        # Create the login frame
        self.create_login_frame()
    
    def create_login_frame(self):
        # Clear any existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Login Frame
        self.login_frame = ttk.Frame(self.root, padding=20)
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.login_frame, text="Resort Booking System", font=("Arial", 24))
        title_label.pack(pady=20)
        
        # Login Form
        login_form = ttk.LabelFrame(self.login_frame, text="Login", padding=20)
        login_form.pack(padx=50, pady=10, fill=tk.X)
        
        # Username
        ttk.Label(login_form, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(login_form, width=30)
        self.username_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Password
        ttk.Label(login_form, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(login_form, width=30, show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Login Button
        login_button = ttk.Button(login_form, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Register Form
        register_form = ttk.LabelFrame(self.login_frame, text="Register New Account", padding=20)
        register_form.pack(padx=50, pady=10, fill=tk.X)
        
        # Username
        ttk.Label(register_form, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reg_username_entry = ttk.Entry(register_form, width=30)
        self.reg_username_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Password
        ttk.Label(register_form, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_password_entry = ttk.Entry(register_form, width=30, show="*")
        self.reg_password_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Email
        ttk.Label(register_form, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_email_entry = ttk.Entry(register_form, width=30)
        self.reg_email_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Phone
        ttk.Label(register_form, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_phone_entry = ttk.Entry(register_form, width=30)
        self.reg_phone_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Register Button
        register_button = ttk.Button(register_form, text="Register", command=self.register)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        
        user_id = login_user(username, password)
        
        if user_id:
            self.user_id = user_id
            self.username = username
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    
    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        email = self.reg_email_entry.get()
        phone = self.reg_phone_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return
        
        if register_user(username, password, email, phone):
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            
            # Clear registration fields
            self.reg_username_entry.delete(0, tk.END)
            self.reg_password_entry.delete(0, tk.END)
            self.reg_email_entry.delete(0, tk.END)
            self.reg_phone_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Username already exists. Please choose another username.")
    
    def create_main_menu(self):
        # Clear any existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create menu frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with welcome message
        title_label = ttk.Label(self.main_frame, text=f"Welcome, {self.username}!", font=("Arial", 18))
        title_label.pack(pady=10)
        
        # Create a notebook (tabbed interface)
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # Create tabs
        self.tab_browse = ttk.Frame(self.tab_control)
        self.tab_bookings = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_browse, text="Browse Rooms")
        self.tab_control.add(self.tab_bookings, text="My Bookings")
        
        self.tab_control.pack(expand=1, fill=tk.BOTH)
        
        # Populate the Browse tab
        self.setup_browse_tab()
        
        # Populate the Bookings tab
        self.setup_bookings_tab()
        
        # Logout button at the bottom
        logout_button = ttk.Button(self.main_frame, text="Logout", command=self.logout)
        logout_button.pack(pady=10)
    
    def setup_browse_tab(self):
        # Date selection frame
        date_frame = ttk.LabelFrame(self.tab_browse, text="Select Dates", padding=10)
        date_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Check-in date
        ttk.Label(date_frame, text="Check-in Date:").grid(row=0, column=0, padx=5, pady=5)
        self.check_in_date = DateEntry(date_frame, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.check_in_date.grid(row=0, column=1, padx=5, pady=5)
        
        # Check-out date
        ttk.Label(date_frame, text="Check-out Date:").grid(row=0, column=2, padx=5, pady=5)
        self.check_out_date = DateEntry(date_frame, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.check_out_date.grid(row=0, column=3, padx=5, pady=5)
        
        # Set default check-out date to the day after check-in
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        self.check_out_date.set_date(tomorrow)
        
        # Search button
        search_button = ttk.Button(date_frame, text="Search Available Rooms", command=self.search_rooms)
        search_button.grid(row=0, column=4, padx=10, pady=5)
        
        # Create a frame for the room list
        self.rooms_frame = ttk.LabelFrame(self.tab_browse, text="Available Rooms", padding=10)
        self.rooms_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for rooms
        self.rooms_tree = ttk.Treeview(self.rooms_frame, columns=("id", "type", "price", "capacity", "description"), show="headings")
        self.rooms_tree.heading("id", text="ID")
        self.rooms_tree.heading("type", text="Room Type")
        self.rooms_tree.heading("price", text="Price/Night")
        self.rooms_tree.heading("capacity", text="Capacity")
        self.rooms_tree.heading("description", text="Description")
        
        self.rooms_tree.column("id", width=50)
        self.rooms_tree.column("type", width=100)
        self.rooms_tree.column("price", width=100)
        self.rooms_tree.column("capacity", width=100)
        self.rooms_tree.column("description", width=400)
        
        self.rooms_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.rooms_tree, orient="vertical", command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Book button
        book_button = ttk.Button(self.rooms_frame, text="Book Selected Room", command=self.book_selected_room)
        book_button.pack(pady=10)
    
    def setup_bookings_tab(self):
        # Create a frame for the bookings list
        self.bookings_frame = ttk.Frame(self.tab_bookings, padding=10)
        self.bookings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_button = ttk.Button(self.bookings_frame, text="Refresh Bookings", command=self.refresh_bookings)
        refresh_button.pack(pady=5, anchor=tk.W)
        
        # Create treeview for bookings
        self.bookings_tree = ttk.Treeview(self.bookings_frame, 
                                         columns=("id", "room_type", "price", "check_in", "check_out", "status"), 
                                         show="headings")
        self.bookings_tree.heading("id", text="ID")
        self.bookings_tree.heading("room_type", text="Room Type")
        self.bookings_tree.heading("price", text="Price/Night")
        self.bookings_tree.heading("check_in", text="Check-in")
        self.bookings_tree.heading("check_out", text="Check-out")
        self.bookings_tree.heading("status", text="Status")
        
        self.bookings_tree.column("id", width=50)
        self.bookings_tree.column("room_type", width=100)
        self.bookings_tree.column("price", width=100)
        self.bookings_tree.column("check_in", width=100)
        self.bookings_tree.column("check_out", width=100)
        self.bookings_tree.column("status", width=100)
        
        self.bookings_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.bookings_tree, orient="vertical", command=self.bookings_tree.yview)
        self.bookings_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.bookings_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Cancel booking button
        cancel_button = ttk.Button(buttons_frame, text="Cancel Selected Booking", command=self.cancel_selected_booking)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Modify booking button
        modify_button = ttk.Button(buttons_frame, text="Modify Selected Booking", command=self.show_modify_booking_dialog)
        modify_button.pack(side=tk.LEFT, padx=5)
        
        # Load bookings
        self.refresh_bookings()
    
    def search_rooms(self):
        check_in = self.check_in_date.get()
        check_out = self.check_out_date.get()
        
        # Validate dates
        if not validate_date_order(check_in, check_out):
            messagebox.showerror("Error", "Check-out date must be after check-in date.")
            return
        
        # Clear the treeview
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)
        
        # Get available rooms
        rooms = get_available_rooms(check_in, check_out)
        
        if not rooms:
            messagebox.showinfo("No Rooms", "No rooms available for the selected dates.")
            return
        
        # Add rooms to the treeview
        for room in rooms:
            room_id, room_type, price, capacity, description = room
            self.rooms_tree.insert("", tk.END, values=(room_id, room_type, f"${price:.2f}", capacity, description))
    
    def book_selected_room(self):
        selected_item = self.rooms_tree.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "Please select a room to book.")
            return
        
        room_id = self.rooms_tree.item(selected_item[0], "values")[0]
        check_in = self.check_in_date.get()
        check_out = self.check_out_date.get()
        
        # Validate room availability again (in case someone booked it meanwhile)
        if not validate_room_available(room_id, check_in, check_out):
            messagebox.showerror("Error", "This room is no longer available for the selected dates.")
            self.search_rooms()  # Refresh room list
            return
        
        # Book the room
        booking_id = book_room(self.user_id, room_id, check_in, check_out)
        
        if booking_id:
            messagebox.showinfo("Success", f"Booking successful! Your booking ID is: {booking_id}")
            self.search_rooms()  # Refresh room list
            self.refresh_bookings()  # Refresh bookings list
            self.tab_control.select(1)  # Switch to bookings tab
        else:
            messagebox.showerror("Error", "Booking failed. Please try again.")
    
    def refresh_bookings(self):
        # Clear the treeview
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        # Get user bookings
        bookings = get_user_bookings(self.user_id)
        
        if not bookings:
            return
        
        # Add bookings to the treeview
        for booking in bookings:
            booking_id, room_type, price, check_in, check_out, status = booking
            self.bookings_tree.insert("", tk.END, values=(booking_id, room_type, f"${price:.2f}", check_in, check_out, status))
    
    def cancel_selected_booking(self):
        selected_item = self.bookings_tree.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to cancel.")
            return
        
        booking_id = self.bookings_tree.item(selected_item[0], "values")[0]
        
        # Confirm cancellation
        if not messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this booking?"):
            return
        
        # Cancel the booking
        if cancel_booking(booking_id, self.user_id):
            messagebox.showinfo("Success", "Booking cancelled successfully!")
            self.refresh_bookings()
        else:
            messagebox.showerror("Error", "Failed to cancel booking. Please try again.")
    
    def show_modify_booking_dialog(self):
        selected_item = self.bookings_tree.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to modify.")
            return
        
        booking_values = self.bookings_tree.item(selected_item[0], "values")
        booking_id = booking_values[0]
        current_check_in = booking_values[3]
        current_check_out = booking_values[4]
        
        # Create modify dialog
        modify_dialog = tk.Toplevel(self.root)
        modify_dialog.title("Modify Booking")
        modify_dialog.geometry("400x200")
        modify_dialog.grab_set()  # Make dialog modal
        
        # Dialog content
        ttk.Label(modify_dialog, text=f"Modify Booking #{booking_id}", font=("Arial", 12)).pack(pady=10)
        
        dates_frame = ttk.Frame(modify_dialog)
        dates_frame.pack(pady=10)
        
        # Check-in date
        ttk.Label(dates_frame, text="New Check-in Date:").grid(row=0, column=0, padx=5, pady=5)
        new_check_in = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        new_check_in.grid(row=0, column=1, padx=5, pady=5)
        new_check_in.set_date(current_check_in)
        
        # Check-out date
        ttk.Label(dates_frame, text="New Check-out Date:").grid(row=1, column=0, padx=5, pady=5)
        new_check_out = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        new_check_out.grid(row=1, column=1, padx=5, pady=5)
        new_check_out.set_date(current_check_out)
        
        # Save button
        def save_changes():
            new_in_date = new_check_in.get()
            new_out_date = new_check_out.get()
            
            # Validate dates
            if not validate_date_order(new_in_date, new_out_date):
                messagebox.showerror("Error", "Check-out date must be after check-in date.")
                return
            
            # Modify the booking
            if modify_booking(booking_id, self.user_id, new_in_date, new_out_date):
                messagebox.showinfo("Success", "Booking modified successfully!")
                modify_dialog.destroy()
                self.refresh_bookings()
            else:
                messagebox.showerror("Error", "Failed to modify booking. Room may not be available for the new dates.")
        
        save_button = ttk.Button(modify_dialog, text="Save Changes", command=save_changes)
        save_button.pack(pady=10)
    
    def logout(self):
        self.user_id = None
        self.username = None
        self.create_login_frame()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ResortBookingApp(root)
    root.mainloop()