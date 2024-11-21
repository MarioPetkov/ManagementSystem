import tkinter as tk
from tkinter import ttk

from appointment_view import AppointmentView
from customer_history import CustomerHistoryView
from database import Database
from customer_view import CustomerView
from employee_history import EmployeeHistoryView
from employee_view import EmployeeView
from history_view import AppointmentsHistory
from material_view import MaterialView
from service_view import ServiceView


class MainApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")
        self.center()
        self.setup_views()

    def center(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 920
        window_height = 520

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.title("Customer management system")

    def setup_views(self):
        EmployeeView(self.notebook, self.db)
        CustomerView(self.notebook, self.db)
        MaterialView(self.notebook, self.db)
        ServiceView(self.notebook, self.db)
        AppointmentView(self.notebook, self.db)
        AppointmentsHistory(self.notebook, self.db)
        EmployeeHistoryView(self.notebook, self.db)
        CustomerHistoryView(self.notebook, self.db)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    app.run()
