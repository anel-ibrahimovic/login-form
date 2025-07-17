import json
import time
import tkinter as tk

class Authenticator:
    LOCKOUT_DURATION = 120

    def __init__(self, filename):
        self.filename = filename
        self.login_data = self.load_data()
        self.attempts = 0
        self.locked_until = 0

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading login data: {e}")
            return {}

    def is_locked(self):
        return time.time() < self.locked_until

    def authentication(self, username, password):
        if self.is_locked():
            return "locked"

        for role, credentials in self.login_data.items():
            if credentials["username"] == username and credentials["password"] == password:
                self.attempts = 0
                self.locked_until = 0
                return role

        self.attempts += 1

        if self.attempts >= 3:
            self.locked_until = time.time() + self.LOCKOUT_DURATION
            return "locked"

        return None

class loginForm:
    def __init__(self, master, authenticator):
        self.master = master
        self.authenticator = authenticator
        self.master.title("Login")
        self.master.geometry("800x500")

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=(0, 10))

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=(0, 5))

        self.show_password = tk.Checkbutton(master, text="Show Password", command=self.toggle_password)
        self.show_password.pack(pady=10)

        self.login_button = tk.Button(master, text="Login", fg="black", bg="white", command=self.login)
        self.login_button.pack(pady=10)

        self.login_message = tk.Label(master, text="", fg="green")
        self.login_message.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.login_message.config(text="Please enter both username and password", fg="red")
            return

        result = self.authenticator.authentication(username, password)

        if result == "locked":
            self.login_message.config(text="Too many attempts. Wait 2 minutes before trying again.", fg="red")
            self.login_button.config(state=tk.DISABLED)
            self.master.after(self.authenticator.LOCKOUT_DURATION * 1000, self.enable_login)
        elif result:
            self.login_message.config(text="Login Successful", fg="green")
            self.open_index_page(result, username)
        else:
            self.login_message.config(text="Login Failed", fg="red")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def enable_login(self):
        self.login_button.config(state=tk.NORMAL)
        self.login_message.config(text="You can try logging in again.", fg="green")

    def toggle_password(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def open_index_page(self, role, username):
        self.master.destroy()
        index_root = tk.Tk()
        index_page = IndexPage(index_root, role, username)
        index_root.mainloop()

class IndexPage:
    def __init__(self, master, role, username):
        self.master = master
        self.master.title("Home")
        self.master.geometry("800x500")

        welcome_message = f"Welcome {username}!"

        self.welcome_label = tk.Label(master, text=welcome_message, font=("Arial", 24))
        self.welcome_label.pack(pady=20)

        self.logout_button = tk.Button(master, text="Logout", command=self.logout)
        self.logout_button.pack(pady=20)

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        auth = Authenticator("login.json")
        app = loginForm(root, auth)
        root.mainloop()

def main():
    root = tk.Tk()
    auth = Authenticator("login.json")
    app = loginForm(root, auth)
    root.mainloop()

if __name__ == "__main__":
    main()
