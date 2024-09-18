import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# Connect to the database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
''')

# Add user function
def add_user():
    name = simpledialog.askstring("Input", "Enter name:")
    if name is None:
        return  # User canceled
    try:
        age = int(simpledialog.askstring("Input", "Enter age:"))
        cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        messagebox.showinfo("Success", "User added successfully.")
        list_users()  # Refresh user list
    except ValueError:
        messagebox.showerror("Error", "Age must be a valid number.")

# Update user function
def update_user():
    user_id = simpledialog.askinteger("Input", "Enter user ID to update:")
    if user_id is None:
        return  # User canceled
    name = simpledialog.askstring("Input", "Enter new name:")
    if name is None:
        return  # User canceled
    try:
        age = int(simpledialog.askstring("Input", "Enter new age:"))
        cursor.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, user_id))
        conn.commit()
        messagebox.showinfo("Success", "User updated successfully.")
        list_users()  # Refresh user list
    except ValueError:
        messagebox.showerror("Error", "Age must be a valid number.")

# Delete user function
def delete_user():
    user_id = simpledialog.askinteger("Input", "Enter user ID to delete:")
    if user_id is None:
        return  # User canceled
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    messagebox.showinfo("Success", "User deleted successfully.")
    list_users()  # Refresh user list

# List users function
def list_users():
    # Clear the listbox
    listbox.delete(0, tk.END)

    # Fetch all users from the database
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    # Insert users into the listbox
    for row in rows:
        listbox.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

# Create the main application window
root = tk.Tk()
root.title("User Management")

# Create buttons for CRUD operations
btn_add = tk.Button(root, text="Add User", command=add_user)
btn_add.pack(pady=5)

btn_update = tk.Button(root, text="Update User", command=update_user)
btn_update.pack(pady=5)

btn_delete = tk.Button(root, text="Delete User", command=delete_user)
btn_delete.pack(pady=5)

btn_list = tk.Button(root, text="List Users", command=list_users)
btn_list.pack(pady=5)

# Create a listbox to display users
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Load users when the application starts
list_users()

# Run the main event loop
root.mainloop()

# Close the database connection when the GUI is closed
conn.close()
