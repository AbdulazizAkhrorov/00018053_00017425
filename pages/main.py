import tkinter as tk
from tkinter import messagebox
import json
from random import randint
from datetime import datetime
from login import LoginPage

class AttendanceManager:

    def __init__(self):
        self.attendance_records = {"CS": {}, "IMOB": {}, "WT": {}}
        self.load_attendance_data()

    def load_attendance_data(self):

        try:
            with open("attendance_data.json", "r") as f:
                self.attendance_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading attendance data: {e}")
            self.attendance_records = {"CS": {}, "IMOB": {}, "WT": {}}

    def save_attendance_data(self):

        try:
            with open("attendance_data.json", "w") as f:
                json.dump(self.attendance_records, f, indent=4)
        except IOError as e:
            print(f"Error saving attendance data: {e}")

    def get_attendance_for_group(self, module, group):

        return self.attendance_records.get(module, {}).get(group, {})

    def update_attendance(self, module, group, date, attended_students, not_attended_students):

        if date not in self.attendance_records[module][group]:
            self.attendance_records[module][group][date] = {"attended": [], "not_attended": []}

        self.attendance_records[module][group][date]["attended"] = attended_students
        self.attendance_records[module][group][date]["not_attended"] = not_attended_students
        self.save_attendance_data()


class StudentGenerator:

    @staticmethod
    def generate_random_students(n):
        first_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack", "Kenny",
                       "Laura", "Maggie", "Nancy", "Oscar", "Paul", "Quincy", "Rachel", "Sophie", "Tom"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "García", "Rodriguez",
                      "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
                      "Jackson", "Martin"]

        return [f"{first_names[randint(0, len(first_names) - 1)]} {last_names[randint(0, len(last_names) - 1)]}"
                for _ in range(n)]


class AttendanceApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.root.geometry("820x700")
        self.root.config(bg="#e3f2fd")


        self.attendance_manager = AttendanceManager()


        self.modules = ["Computer Science", "IMOB", "Web Technology"]
        self.groups = ["Group 1", "Group 2", "Group 3"]
        self.students = StudentGenerator.generate_random_students(15)
        self.module_students = {module: {group: self.students for group in self.groups} for module in self.modules}

        self.setup_ui()

    def setup_ui(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.module_label = tk.Label(self.root, text="Select Module", font=("Arial", 16, "bold"), bg="#2196f3", fg="#ffffff")
        self.module_label.pack(pady=20, fill="x")

        self.module_var = tk.StringVar(self.root, value=self.modules[0])
        self.module_menu = tk.OptionMenu(self.root, self.module_var, *self.modules)
        self.module_menu.config(font=("Arial", 12), bg="#ffffff", fg="#01579b")
        self.module_menu.pack(pady=10)

        self.select_module_button = tk.Button(self.root, text="Select Module", font=("Arial", 12), bg="#2196f3", fg="#ffffff", command=self.show_group_window)
        self.select_module_button.pack(pady=10)

    def show_group_window(self):

        selected_module = self.module_var.get()
        self.attendance_manager.attendance_records.setdefault(selected_module, {})

        self.show_group_selection(selected_module)

    def show_group_selection(self, selected_module):

        self.attendance_label = tk.Label(self.root, text=f"Attendance for {selected_module}", font=("Arial", 16, "bold"), bg="#2196f3", fg="#ffffff")
        self.attendance_label.pack(pady=20, fill="x")

        self.group_var = tk.StringVar(self.root, value=self.groups[0])
        self.group_menu = tk.OptionMenu(self.root, self.group_var, *self.groups)
        self.group_menu.config(font=("Arial", 12), bg="#ffffff", fg="#01579b")
        self.group_menu.pack(pady=10)

        self.select_group_button = tk.Button(self.root, text="Select Group", font=("Arial", 12), bg="#2196f3", fg="#ffffff", command=lambda: self.show_attendance_check_window(selected_module))
        self.select_group_button.pack(pady=10)

    def show_attendance_check_window(self, selected_module):

        selected_group = self.group_var.get()
        self.show_attendance_check_window_for_group(selected_module, selected_group)

    def show_attendance_check_window_for_group(self, selected_module, selected_group):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.attendance_label = tk.Label(self.root, text=f"Attendance for {selected_module} - {selected_group}", font=("Arial", 16, "bold"), bg="#2196f3", fg="#ffffff")
        self.attendance_label.pack(pady=20, fill="x")

        self.attendance_vars = {}
        students_in_group = self.module_students[selected_module][selected_group]

        self.checkbox_frame = tk.Frame(self.root, bg="#e3f2fd")
        self.checkbox_frame.pack(pady=5)

        for student in students_in_group:
            var = tk.IntVar()
            self.attendance_vars[student] = var
            checkbox = tk.Checkbutton(self.checkbox_frame, text=student, font=("Arial", 12), variable=var, bg="#e3f2fd", fg="#01579b")
            checkbox.pack(anchor="w", pady=2)

        self.submit_button = tk.Button(self.root, text="Submit Attendance", font=("Arial", 12), bg="#2196f3", fg="#ffffff", command=lambda: self.submit_attendance(selected_module, selected_group))
        self.submit_button.pack(pady=20)

        self.view_button = tk.Button(self.root, text="View Attendance", font=("Arial", 12), bg="#2196f3", fg="#ffffff", command=lambda: self.view_attendance(selected_module, selected_group))
        self.view_button.pack(pady=10)

    def submit_attendance(self, selected_module, selected_group):

        attended_students = [student for student, var in self.attendance_vars.items() if var.get() == 1]
        not_attended_students = [student for student, var in self.attendance_vars.items() if var.get() == 0]

        current_date = datetime.now().strftime("%A, %B %d, %Y")


        if selected_module not in self.attendance_manager.attendance_records:
            self.attendance_manager.attendance_records[selected_module] = {}

        if selected_group not in self.attendance_manager.attendance_records[selected_module]:
            self.attendance_manager.attendance_records[selected_module][selected_group] = {}


        if current_date not in self.attendance_manager.attendance_records[selected_module][selected_group]:
            self.attendance_manager.attendance_records[selected_module][selected_group][current_date] = {"attended": [],
                                                                                                         "not_attended": []}


        self.attendance_manager.attendance_records[selected_module][selected_group][current_date][
            "attended"] = attended_students
        self.attendance_manager.attendance_records[selected_module][selected_group][current_date][
            "not_attended"] = not_attended_students


        self.attendance_manager.save_attendance_data()

        messagebox.showinfo("Attendance Submitted",
                            f"Attendance for {selected_group} in {selected_module} submitted successfully.")

    def view_attendance(self, selected_module, selected_group):

        attendance_data = self.attendance_manager.get_attendance_for_group(selected_module, selected_group)

        view_window = tk.Toplevel(self.root)
        view_window.title(f"Attendance History - {selected_module} - {selected_group}")
        view_window.geometry("900x900")

        history_label = tk.Label(view_window, text="Attendance History", font=("Arial", 14, "bold"), bg="#2196f3", fg="#ffffff")
        history_label.pack(pady=10, fill="x")

        for date, record in sorted(attendance_data.items(), reverse=True):
            date_label = tk.Label(view_window, text=f"Date: {date}", font=("Arial", 12, "bold"), bg="#ffffff", fg="#01579b")
            date_label.pack(pady=5)

            attended_label = tk.Label(view_window, text="Attended Students", font=("Arial", 12), bg="#ffffff", fg="#01579b")
            attended_label.pack(pady=5)
            attended_students = "\n".join(record["attended"]) if record["attended"] else "None"
            attended_list = tk.Label(view_window, text=attended_students, font=("Arial", 12), bg="#ffffff", fg="#01579b")
            attended_list.pack(pady=5)

            not_attended_label = tk.Label(view_window, text="Not Attended Students", font=("Arial", 12), bg="#ffffff", fg="#01579b")
            not_attended_label.pack(pady=5)
            not_attended_students = "\n".join(record["not_attended"]) if record["not_attended"] else "None"
            not_attended_list = tk.Label(view_window, text=not_attended_students, font=("Arial", 12), bg="#ffffff", fg="#01579b")
            not_attended_list.pack(pady=5)

        close_button = tk.Button(view_window, text="Close", font=("Arial", 12), bg="#f44336", fg="#ffffff", command=view_window.destroy)
        close_button.pack(pady=20)


def on_login_success():

    login_page.root.quit()
    login_page.root.destroy()
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root, on_login_success=on_login_success)
    root.mainloop()
