import tkinter as tk
from tkinter import ttk


class EmployeeHistoryView:
    def __init__(self, notebook, db):
        self.notebook = notebook
        self.db = db
        self.employee_map = {}
        self.selected_employee_id = None

        self.frame_employee_history = ttk.Frame(self.notebook)
        self.frame_employee_history.configure(height=200, padding=15, width=200)
        self.notebook.add(self.frame_employee_history, text="Employee report")

        self.selected_employee_var = tk.StringVar()
        self.selected_employee_var.trace("w", self.populate_employee_appointments)

        self.setup_ui()
        self.populate_employees()

    def setup_ui(self):
        self.lblframe_employee_history = ttk.Labelframe(self.frame_employee_history, text="Employee report")
        self.lblframe_employee_history.configure(padding=10)
        self.lblframe_employee_history.grid(row=0, column=0, sticky="nsew")

        self.employee_label = tk.Label(self.lblframe_employee_history, text="Select:")
        self.employee_menu = ttk.OptionMenu(self.lblframe_employee_history, self.selected_employee_var, "")
        self.employee_menu.config(width=30)

        self.employee_label.grid(row=0, column=0, padx=(2, 2), pady=5, sticky="w")
        self.employee_menu.grid(row=0, column=1, padx=(2, 2), pady=5, sticky="w")

        self.tree = ttk.Treeview(self.lblframe_employee_history,
                                 columns=("CustomerFullName", "ServiceName", "AppointmentDate", "Status", "Notes"),
                                 show='headings', height=12)

        self.tree.heading("CustomerFullName", text="Customer")
        self.tree.heading("ServiceName", text="Service")
        self.tree.heading("AppointmentDate", text="Date")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Notes", text="Note")

        self.tree.column("CustomerFullName", width=150)
        self.tree.column("ServiceName", width=120)
        self.tree.column("AppointmentDate", width=100)
        self.tree.column("Status", width=50)
        self.tree.column("Notes", width=170)

        self.tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.lblframe_employee_history, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.lblframe_employee_history.grid_columnconfigure(0, weight=1)
        self.lblframe_employee_history.grid_rowconfigure(1, weight=1)

        # Add readonly fields for earnings
        self.earned_all_time_var = tk.StringVar(value="0.00")
        self.earned_last_30_days_var = tk.StringVar(value="0.00")
        self.earned_last_7_days_var = tk.StringVar(value="0.00")

        self.money_spent_all_time_var = tk.StringVar(value="0.00")
        self.money_spent_last_30_days_var = tk.StringVar(value="0.00")
        self.money_spent_last_7_days_var = tk.StringVar(value="0.00")

        # First Column: Earned labels and fields
        self.earned_all_time_label = ttk.Label(self.lblframe_employee_history, text="Revenue (Total)")
        self.earned_all_time_entry = ttk.Entry(self.lblframe_employee_history, textvariable=self.earned_all_time_var, state="readonly", width=15)

        self.earned_last_30_days_label = ttk.Label(self.lblframe_employee_history, text="Revenue (Last 30 days)")
        self.earned_last_30_days_entry = ttk.Entry(self.lblframe_employee_history, textvariable=self.earned_last_30_days_var, state="readonly", width=15)

        self.earned_last_7_days_label = ttk.Label(self.lblframe_employee_history, text="Revenue (Last 7 days)")
        self.earned_last_7_days_entry = ttk.Entry(self.lblframe_employee_history, textvariable=self.earned_last_7_days_var, state="readonly", width=15)

        # Second Column: Money spent labels and fields
        self.money_spent_all_time_label = ttk.Label(self.lblframe_employee_history, text="Expense (Total)")
        self.money_spent_all_time_entry = ttk.Entry(self.lblframe_employee_history, textvariable=self.money_spent_all_time_var, state="readonly", width=15)

        self.money_spent_last_30_days_label = ttk.Label(self.lblframe_employee_history, text="Expense (Last 30 days)")
        self.money_spent_last_30_days_entry = ttk.Entry(self.lblframe_employee_history, textvariable=self.money_spent_last_30_days_var, state="readonly", width=15)

        self.money_spent_last_7_days_label = ttk.Label(self.lblframe_employee_history, text="Разход (Last 7 days)")
        self.money_spent_last_7_days_entry = ttk.Entry(self.lblframe_employee_history, textvariable=self.money_spent_last_7_days_var, state="readonly", width=15)

        # Positioning for Earned fields
        self.earned_all_time_label.grid(row=2, column=0, padx=(2, 2), pady=5, sticky="w")
        self.earned_all_time_entry.grid(row=2, column=1, padx=(2, 2), pady=5, sticky="w")

        self.earned_last_30_days_label.grid(row=3, column=0, padx=(2, 2), pady=5, sticky="w")
        self.earned_last_30_days_entry.grid(row=3, column=1, padx=(2, 2), pady=5, sticky="w")

        self.earned_last_7_days_label.grid(row=4, column=0, padx=(2, 2), pady=5, sticky="w")
        self.earned_last_7_days_entry.grid(row=4, column=1, padx=(2, 2), pady=5, sticky="w")

        # Positioning for Money Spent fields
        self.money_spent_all_time_label.grid(row=2, column=2, padx=(2, 2), pady=5, sticky="w")
        self.money_spent_all_time_entry.grid(row=2, column=3, padx=(2, 2), pady=5, sticky="w")

        self.money_spent_last_30_days_label.grid(row=3, column=2, padx=(2, 2), pady=5, sticky="w")
        self.money_spent_last_30_days_entry.grid(row=3, column=3, padx=(2, 2), pady=5, sticky="w")

        self.money_spent_last_7_days_label.grid(row=4, column=2, padx=(2, 2), pady=5, sticky="w")
        self.money_spent_last_7_days_entry.grid(row=4, column=3, padx=(2, 2), pady=5, sticky="w")

    def populate_employees(self):
        employees = self.db.get_existing_employees()
        employees_sorted = sorted(employees, key=lambda e: e['FirstName'])
        menu = self.employee_menu["menu"]
        menu.delete(0, "end")

        for employee in employees_sorted:
            employee_fullname = f"{employee['FirstName']} {employee['LastName']}"
            self.employee_map[employee['EmployeeID']] = employee_fullname
            menu.add_command(label=employee_fullname, command=lambda value=employee['EmployeeID']: self.on_employee_selected(value))

    def on_employee_selected(self, employee_id):
        self.selected_employee_id = employee_id
        full_name = self.employee_map[employee_id]
        self.selected_employee_var.set(full_name)
        self.populate_employee_appointments()
        # Populate earnings
        earnings = self.db.get_employee_earnings(employee_id)
        self.earned_all_time_var.set(f"{earnings['total_earnings']:.2f}")
        self.earned_last_30_days_var.set(f"{earnings['last_30_days_earnings']:.2f}")
        self.earned_last_7_days_var.set(f"{earnings['last_7_days_earnings']:.2f}")

        # Populate money spent
        money_spent = self.db.get_money_invested(employee_id)
        self.money_spent_all_time_var.set(f"{money_spent['total_spent']:.2f}")
        self.money_spent_last_30_days_var.set(f"{money_spent['last_30_days_spent']:.2f}")
        self.money_spent_last_7_days_var.set(f"{money_spent['last_7_days_spent']:.2f}")

    def populate_employee_appointments(self, *args):
        if self.selected_employee_id:
            results = self.db.get_employee_appointments(self.selected_employee_id)
            self.display_results(results)

    def populate_employee_earnings(self):
        if self.selected_employee_id:
            earnings = self.db.get_employee_earnings(self.selected_employee_id)
            self.earned_all_time_var.set(f"{earnings['total_earnings']:.2f}")
            self.earned_last_30_days_var.set(f"{earnings['last_30_days_earnings']:.2f}")
            self.earned_last_7_days_var.set(f"{earnings['last_7_days_earnings']:.2f}")

    def populate_money_spent(self):
        if self.selected_employee_id:
            money_spent = self.db.get_money_invested(self.selected_employee_id)
            self.money_spent_all_time_var.set(f"{money_spent['total_spent']:.2f}")
            self.money_spent_last_30_days_var.set(f"{money_spent['last_30_days_spent']:.2f}")
            self.money_spent_last_7_days_var.set(f"{money_spent['last_7_days_spent']:.2f}")

    def display_results(self, results):
        self.tree.delete(*self.tree.get_children())

        if results:
            for result in results:
                row = (f"{result.get('CustomerFirstName', '')} {result.get('CustomerLastName', '')}",
                       result.get("ServiceName", ""),
                       result.get("AppointmentDate", ""),
                       result.get("Status", ""),
                       result.get("Notes", ""))
                self.tree.insert("", tk.END, values=row)