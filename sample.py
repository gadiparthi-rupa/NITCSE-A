import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

CSV_FILE = "students.csv"

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Information Management System")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e2f4f")  # Dark blue background

        # Fonts and colors
        self.label_font = ("Segoe UI", 12, "bold")
        self.entry_font = ("Segoe UI", 11)
        self.button_font = ("Segoe UI", 11, "bold")
        self.text_color = "white"
        self.entry_bg = "#f0f0f0"

        # Frame for form
        form_frame = tk.Frame(root, bg="#1e2f4f")
        form_frame.pack(pady=20, padx=30, fill="x")

        # Labels and Entries
        tk.Label(form_frame, text="Name:", font=self.label_font, fg=self.text_color, bg="#1e2f4f").grid(row=0, column=0, sticky="w", padx=5, pady=8)
        tk.Label(form_frame, text="Age:", font=self.label_font, fg=self.text_color, bg="#1e2f4f").grid(row=1, column=0, sticky="w", padx=5, pady=8)
        tk.Label(form_frame, text="Class:", font=self.label_font, fg=self.text_color, bg="#1e2f4f").grid(row=2, column=0, sticky="w", padx=5, pady=8)
        tk.Label(form_frame, text="Contact:", font=self.label_font, fg=self.text_color, bg="#1e2f4f").grid(row=3, column=0, sticky="w", padx=5, pady=8)

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.contact_var = tk.StringVar()

        entry_width = 30
        self.name_entry = tk.Entry(form_frame, textvariable=self.name_var, font=self.entry_font, width=entry_width, bg=self.entry_bg)
        self.age_entry = tk.Entry(form_frame, textvariable=self.age_var, font=self.entry_font, width=entry_width, bg=self.entry_bg)
        self.class_entry = tk.Entry(form_frame, textvariable=self.class_var, font=self.entry_font, width=entry_width, bg=self.entry_bg)
        self.contact_entry = tk.Entry(form_frame, textvariable=self.contact_var, font=self.entry_font, width=entry_width, bg=self.entry_bg)

        self.name_entry.grid(row=0, column=1, padx=10, pady=8)
        self.age_entry.grid(row=1, column=1, padx=10, pady=8)
        self.class_entry.grid(row=2, column=1, padx=10, pady=8)
        self.contact_entry.grid(row=3, column=1, padx=10, pady=8)

        # Buttons frame
        btn_frame = tk.Frame(form_frame, bg="#1e2f4f")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        add_btn = tk.Button(btn_frame, text="Add Student", font=self.button_font, bg="#3a71c1", fg="white", activebackground="#255e9f", activeforeground="white", padx=15, pady=8, command=self.add_student, borderwidth=0)
        clear_btn = tk.Button(btn_frame, text="Clear Fields", font=self.button_font, bg="#6c757d", fg="white", activebackground="#5a6268", activeforeground="white", padx=15, pady=8, command=self.clear_fields, borderwidth=0)

        add_btn.grid(row=0, column=0, padx=10)
        clear_btn.grid(row=0, column=1, padx=10)

        # Treeview frame with label
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10, padx=30, fill="both", expand=True)

        tk.Label(list_frame, text="Student Records", font=("Segoe UI", 14, "bold"), fg="#1e2f4f").pack(anchor="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="white",
                        font=("Segoe UI", 11))
        style.map('Treeview', background=[('selected', '#3a71c1')], foreground=[('selected', 'white')])

        columns = ("Name", "Age", "Class", "Contact")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Name":
                self.tree.column(col, width=200)
            elif col == "Age":
                self.tree.column(col, width=70, anchor="center")
            elif col == "Class":
                self.tree.column(col, width=100, anchor="center")
            else:
                self.tree.column(col, width=180)

        self.tree.pack(fill="both", expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Load existing students
        self.load_students()

    def add_student(self):
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        class_ = self.class_var.get().strip()
        contact = self.contact_var.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Validation Error", "Name cannot be empty.")
            return
        if age and not age.isdigit():
            messagebox.showerror("Validation Error", "Age must be a number.")
            return

        # Add to treeview
        self.tree.insert("", "end", values=(name, age, class_, contact))

        # Save to CSV
        self.save_students()

        # Clear inputs
        self.clear_fields()

    def clear_fields(self):
        self.name_var.set("")
        self.age_var.set("")
        self.class_var.set("")
        self.contact_var.set("")

    def save_students(self):
        rows = [self.tree.item(child)["values"] for child in self.tree.get_children()]
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Age", "Class", "Contact"])
            writer.writerows(rows)

    def load_students(self):
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode="r") as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                for row in reader:
                    if len(row) == 4:
                        self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()



