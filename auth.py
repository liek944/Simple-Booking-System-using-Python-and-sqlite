# auth.py
from database import db_connection

# Function to register a new user
def register_user(username, password, email=None, phone=None):
    with db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return False
        
        try:
            cursor.execute(
                'INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)',
                (username, password, email, phone)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Registration error: {e}")
            return False

# Function to log in a user
def login_user(username, password):
    with db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        
        if user:
            return user[0]  # Return the user ID
        else:
            return None

# Function to get user profile
def get_user_profile(user_id):
    with db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, email, phone FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

# Function to update user profile
def update_user_profile(user_id, email=None, phone=None, password=None):
    with db_connection() as conn:
        cursor = conn.cursor()
        
        try:
            if password:
                cursor.execute('UPDATE users SET password = ? WHERE id = ?', (password, user_id))
            
            if email:
                cursor.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
            
            if phone:
                cursor.execute('UPDATE users SET phone = ? WHERE id = ?', (phone, user_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Profile update error: {e}")
            conn.rollback()
            return False