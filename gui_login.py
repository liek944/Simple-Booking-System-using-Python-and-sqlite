import tkinter as tk
from tkinter import messagebox
from auth import login_user

# Function to handle login
def on_login():
    username = entry_username.get()
    password = entry_password.get()

    user_id = login_user(username, password)
    if user_id:
        messagebox.showinfo("Login Successful", f"Welcome, User ID: {user_id}!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Create the main window
root = tk.Tk()
root.title("Resort Booking System - Login")

# Username label and entry
label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

# Password label and entry
label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Login button
button_login = tk.Button(root, text="Login", command=on_login)
button_login.pack()

# Run the application
root.mainloop()