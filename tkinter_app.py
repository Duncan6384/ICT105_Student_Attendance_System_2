from cmath import e
import datetime
import email
import tkinter as tk
from tkinter import Tk, messagebox
import sqlite3
from werkzeug.security import generate_password_hash
import logging

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a user
def add_user(username, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username or email already exists.")
    except Exception as e:
        logging.error(f"An error occurred while adding user {username}: {str(e)}")
        messagebox.showerror("Error", f"An unexpected error occurred. Please try again.: {str(e)}")
    finally:
        conn.close()

# Function to check if username or email is taken
def is_username_or_email_taken(username, email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT (*) FROM users WHERE username=? OR email=?', (username, email))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# Function to handle the registration button click
def register():
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()
    if username and email and password:
        if is_username_or_email_taken(username, email):
            messagebox.showerror("Error", "Username or email already exists. Please log in.")
        else:
            add_user(username, email, password)
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

# Function to add attendance
def mark_attendance(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    try:
        cursor.execute('INSERT INTO attendance (user_id, date) VALUES (?, ?)', (user_id, date))
        conn.commit()
        messagebox.showinfo("Success", "Attendance marked successfully!")
    except Exception as e:
        logging.error(f"An error occurred while marking attendance for user ID {user_id}: {str(e)}")
        messagebox.showerror("Error", "An unexpected error occurred while marking attendance.")
    finally:
        conn.close()

# Function to check attendance
def check_attendance(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date FROM attendance WHERE user_id=?', (user_id,))
    record = cursor.fetchall()
    conn.close()
    if record:
        attendance_dates = [record[e][0] for e in range(len(record))]
        messagebox.showinfo("Attendance Records", f"Attendance Dates: {', '.join(attendance_dates)}")
    else:
        messagebox.showinfo("Attendance Records", "No attendance records found.")

# Function to get user ID from username
def get_user_id(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username=?', (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

# Prepare user data
users_data = [
    (1001, 'Alice Smith', 'sd1001@uni123st.edu.au'),
    (1002, 'Bob Johnson', 'sd1002@uni123st.edu.au'),
    (1003, 'Charlie Brown', 'sd1003@uni123st.edu.au'),
    (1004, 'David Lee', 'sd1004@uni123st.edu.au'),
    (1005, 'Emily Davis', 'sd1005@uni123st.edu.au'),
    (1006, 'Frank Wilson', 'sd1006@uni123st.edu.au'),
    (1007, 'Grace Taylor', 'sd1007@uni123st.edu.au'),
    (1008, 'Henry Anderson', 'sd1008@uni123st.edu.au'),
    (1009, 'Isabella Thomas', 'sd1009@uni123st.edu.au'),
    (1010, 'Jack Hill', 'sd1010@uni123st.edu.au'),
    (1011, 'Kate Baker', 'sd1011@uni123st.edu.au'),
    (1012, 'Liam Carter', 'sd1012@uni123st.edu.au'),
    (1013, 'Maria Evans', 'sd1013@uni123st.edu.au'),
    (1014, 'Noah Robinson', 'sd1014@uni123st.edu.au'),
    (1015, 'Olivia Lewis', 'sd1015@uni123st.edu.au'),
    (1016, 'Parker Allen', 'sd1016@uni123st.edu.au'),
    (1017, 'Quinn Williams', 'sd1017@uni123st.edu.au'),
    (1018, 'Riley Jones', 'sd1018@uni123st.edu.au'),
    (1019, 'Sophia Clark', 'sd1019@uni123st.edu.au'),
    (1020, 'Tyler Brown', 'sd1020@uni123st.edu.au'),
]

# Create the GUI
root = tk.Tk()
root.title("User Registration and Attendance System")

# Create and place the label and entry fields
label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_email = tk.Label(root, text="Email:")
label_email.pack()
entry_email = tk.Entry(root)
entry_email.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Create and place the register button
button_register = tk.Button(root, text="Register", command=register)
button_register.pack()

# Create and place attendance section
label_attendance_username = tk.Label(root, text="Username for Attendance:")
label_attendance_username.pack()
entry_attendance_username = tk.Entry(root)
entry_attendance_username.pack()

# Button to mark attendance
button_mark_attendance = tk.Button(root, text="Mark Attendance", command=lambda: mark_attendance(get_user_id(entry_attendance_username.get())))
button_mark_attendance.pack()

# Button to check attendance
button_check_attendance = tk.Button(root, text="Check Attendance", command=lambda: check_attendance(get_user_id(entry_attendance_username.get())))
button_check_attendance.pack()

# Initialize the database
init_db()

# Start the GUI event loop
root.mainloop()