import tkinter as tk
from tkinter import messagebox, ttk
import json
from random import randint
from datetime import datetime


class MainPage:
    def init(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.root.geometry("820x700")
        self.root.config(bg="#e3f2fd")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.attendance_records = {"CS": {}, "IMOB": {}, "WT": {}}
        self.modules = ["Computer Science", "IMOB", "Web Technology"]


        self.students = self.generate_random_students(15)
        self.groups = ["Group 1", "Group 2", "Group 3"]


        self.module_students = {
            module: {group: self.students for group in self.groups}
            for module in self.modules
        }

        self.load_attendance_data()
        self.module_label = tk.Label(self.root, text="Select Module", font=("Arial", 16, "bold"), bg="#2196f3",
                                     fg="#ffffff")
        self.module_label.pack(pady=20, fill="x")

        self.module_var = tk.StringVar(self.root)
        self.module_var.set(self.modules[0])
        self.module_menu = tk.OptionMenu(self.root, self.module_var, *self.modules)
        self.module_menu.config(font=("Arial", 12), bg="#ffffff", fg="#01579b")
        self.module_menu.pack(pady=10)

        self.select_module_button = tk.Button(self.root, text="Select Module", font=("Arial", 12), bg="#2196f3",
                                              fg="#ffffff", command=self.show_group_window)
        self.select_module_button.pack(pady=10)

    def show_group_window(self):

        selected_module = self.module_var.get()


        if selected_module not in self.attendance_records:
            self.attendance_records[selected_module] = {}


        self.show_group_selection(selected_module)

    def show_group_selection(self, selected_module):


        self.attendance_label = tk.Label(self.root, text=f"Attendance for {selected_module}",
                                         font=("Arial", 16, "bold"), bg="#2196f3", fg="#ffffff")
        self.attendance_label.pack(pady=20, fill="x")


        self.group_var = tk.StringVar(self.root)
        self.group_var.set(self.groups[0])
        self.group_menu = tk.OptionMenu(self.root, self.group_var, *self.groups)
        self.group_menu.config(font=("Arial", 12), bg="#ffffff", fg="#01579b")
        self.group_menu.pack(pady=10)


        self.select_group_button = tk.Button(self.root, text="Select Group", font=("Arial", 12), bg="#2196f3",
                                             fg="#ffffff",
                                             command=lambda: self.show_attendance_check_window(selected_module))
        self.select_group_button.pack(pady=10)

    def show_attendance_check_window(self, selected_module):

        selected_group = self.group_var.get()


        if selected_group not in self.attendance_records[selected_module]:
            self.attendance_records[selected_module][selected_group] = {}


        self.show_attendance_check_window_for_group(selected_module, selected_group)

    def show_attendance_check_window_for_group(self, selected_module, selected_group):


        for widget in self.root.winfo_children():
            widget.destroy()


        self.attendance_label = tk.Label(self.root, text=f"Attendance for {selected_module} - {selected_group}",
                                         font=("Arial", 16, "bold"), bg="#2196f3", fg="#ffffff")
        self.attendance_label.pack(pady=20, fill="x")


        self.attendance_vars = {}
        students_in_group = self.module_students[selected_module][selected_group]

        self.checkbox_frame = tk.Frame(self.root, bg="#e3f2fd")
        self.checkbox_frame.pack(pady=5)
