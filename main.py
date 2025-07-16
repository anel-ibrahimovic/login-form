import tkinter as tk
import json

FILENAME="login.json"

def load_data(FILENAME):
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading login data: {e}")
        return{}

login_data = load_data(FILENAME)

def authentication(username, password):
    for role, credentials in login_data.items():
        if credentials["username"] == username and credentials["password"] == password:
            return role
    return None

root = tk.Tk()
root.title("Login")
root.geometry("800x500")

username_label = tk.Label(root, text="Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=(0, 10))

password_label = tk.Label(root, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=(0, 5))

def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        login_message.config(text="Please enter both username and password")
        return
    role = authentication(username, password)
    if role:
        login_message.config(text="Login Successful", fg="green")
    else:
        login_message.config(text="Login Failed", fg="red")

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

show_password = tk.Checkbutton(root, text="Show Password", command=toggle_password)
show_password.pack(pady=10)

login_button = tk.Button(root, text="Login", fg="black", bg="white", command=login)
login_button.pack(pady=10)

login_message = tk.Label(root, text="", fg="green")
login_message.pack(pady=10)

root.mainloop()
