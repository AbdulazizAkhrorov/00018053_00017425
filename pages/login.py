import tkinter as tk
from tkinter import messagebox

class LoginPage:
    def __init__(self, root, on_login_success):
        """Initialize login page with the title and resolution"""
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login System")
        self.root.geometry("400x600")
        self.root.config(bg="#e3f2fd")

        self.username_label = tk.Label(self.root, text="Enter Username:", font=("Arial", 12), bg="#e3f2fd", fg="#01579b")
        self.username_label.pack(pady=20)

        self.username_entry = tk.Entry(self.root, font=("Arial", 12), bg="#ffffff", fg="#01579b", relief="solid")
        self.username_entry.pack(pady=5)

        self.username_button = tk.Button(self.root, text="Next", font=("Arial", 12), bg="#2196f3", fg="#ffffff", command=self.check_username)
        self.username_button.pack(pady=10)

    def check_username(self):
        username = self.username_entry.get().strip()
        if username == "Abu":
            self.show_password_window()
        else:
            messagebox.showerror("Error", "Incorrect Username. Please try again.")

    def show_password_window(self):
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.username_button.pack_forget()

        self.password_label = tk.Label(self.root, text="Enter Password:", font=("Arial", 12), bg="#e3f2fd", fg="#01579b")
        self.password_label.pack(pady=20)

        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), bg="#ffffff", fg="#01579b", relief="solid")
        self.password_entry.pack(pady=5)

        self.password_button = tk.Button(self.root, text="Login", font=("Arial", 12), bg="#2196f3", fg="#ffffff", command=self.check_password)
        self.password_button.pack(pady=10)

    def check_password(self):
        password = self.password_entry.get().strip()
        if password == "12345":
            messagebox.showinfo("Success", "Login Successful!")
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Incorrect Password. Please try again.")
