import tkinter as tk
from tkinter import messagebox
import sqlite3
from werkzeug.security import generate_password_hash

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a user
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "User  registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

# Function to handle the registration button click
def register():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        add_user(username, password)
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

# Create the main window
root = tk.Tk()
root.title("User  Registration")

# Create and place the labels and entries
label_username = tk.Label(root, text="Username:")
label_username.pack(pady=5)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show='*')
entry_password.pack(pady=5)

# Create and place the register button
button_register = tk.Button(root, text="Register", command=register)
button_register.pack(pady=20)

# Initialize the database
init_db()

# Start the Tkinter event loop
root.mainloop()