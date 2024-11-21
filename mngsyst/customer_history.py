import tkinter as tk
from tkinter import ttk


class CustomerHistoryView:
    def __init__(self, notebook, db):
        self.notebook = notebook
        self.db = db
        self.customer_map = {}
        self.selected_customer_id = None

        self.frame_customer_history = ttk.Frame(self.notebook)
        self.frame_customer_history.configure(height=200, padding=15, width=200)
        self.notebook.add(self.frame_customer_history, text="Customer report")

        self.selected_customer_var = tk.StringVar()
        self.selected_customer_var.trace("w", self.populate_customer_appointments)

        self.setup_ui()
        self.populate_customers()

    def setup_ui(self):
        self.lblframe_customer_history = ttk.Labelframe(self.frame_customer_history, text="Customer report")
        self.lblframe_customer_history.configure(padding=10)
        self.lblframe_customer_history.grid(row=0, column=0, sticky="nsew")

        self.customer_label = tk.Label(self.lblframe_customer_history, text="Select:")
        self.customer_menu = ttk.OptionMenu(self.lblframe_customer_history, self.selected_customer_var, "")
        self.customer_menu.config(width=30)

        self.customer_label.grid(row=0, column=0, padx=(2, 2), pady=5, sticky="w")
        self.customer_menu.grid(row=0, column=1, padx=(2, 2), pady=5, sticky="w")

        self.tree = ttk.Treeview(self.lblframe_customer_history,
                                 columns=("EmployeeFullName", "ServiceName", "AppointmentDate", "Status", "Price", "Notes"),
                                 show='headings', height=12)

        self.tree.heading("EmployeeFullName", text="Employee")
        self.tree.heading("ServiceName", text="Service")
        self.tree.heading("AppointmentDate", text="Date")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Notes", text="Note")

        self.tree.column("EmployeeFullName", width=150)
        self.tree.column("ServiceName", width=150)
        self.tree.column("AppointmentDate", width=120)
        self.tree.column("Status", width=100)
        self.tree.column("Price", width=50)
        self.tree.column("Notes", width=170)

        self.tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.lblframe_customer_history, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.lblframe_customer_history.grid_columnconfigure(0, weight=1)
        self.lblframe_customer_history.grid_rowconfigure(1, weight=1)

        # Add readonly fields for money spent statistics
        self.spent_all_time_var = tk.StringVar(value="0.00")
        self.spent_last_30_days_var = tk.StringVar(value="0.00")
        self.spent_last_7_days_var = tk.StringVar(value="0.00")

        self.appointments_all_time_var = tk.StringVar(value="0")
        self.appointments_last_30_days_var = tk.StringVar(value="0")
        self.appointments_last_7_days_var = tk.StringVar(value="0")

        # First Column: Money spent labels and fields
        self.spent_all_time_label = ttk.Label(self.lblframe_customer_history, text="Spent (Total)")
        self.spent_all_time_entry = ttk.Entry(self.lblframe_customer_history, textvariable=self.spent_all_time_var, state="readonly", width=15)

        self.spent_last_30_days_label = ttk.Label(self.lblframe_customer_history, text="Spent (Last 30 days)")
        self.spent_last_30_days_entry = ttk.Entry(self.lblframe_customer_history, textvariable=self.spent_last_30_days_var, state="readonly", width=15)

        self.spent_last_7_days_label = ttk.Label(self.lblframe_customer_history, text="Spent (Last 7 days)")
        self.spent_last_7_days_entry = ttk.Entry(self.lblframe_customer_history, textvariable=self.spent_last_7_days_var, state="readonly", width=15)

        # Positioning for Money Spent fields
        self.spent_all_time_label.grid(row=2, column=0, padx=(2, 2), pady=5, sticky="w")
        self.spent_all_time_entry.grid(row=2, column=1, padx=(2, 2), pady=5, sticky="w")

        self.spent_last_30_days_label.grid(row=3, column=0, padx=(2, 2), pady=5, sticky="w")
        self.spent_last_30_days_entry.grid(row=3, column=1, padx=(2, 2), pady=5, sticky="w")

        self.spent_last_7_days_label.grid(row=4, column=0, padx=(2, 2), pady=5, sticky="w")
        self.spent_last_7_days_entry.grid(row=4, column=1, padx=(2, 2), pady=5, sticky="w")

        # Positioning for Appointments fields
        self.appointments_all_time_label = ttk.Label(self.lblframe_customer_history, text="Reservations (Total)")
        self.appointments_all_time_entry = ttk.Entry(self.lblframe_customer_history, textvariable=self.appointments_all_time_var, state="readonly", width=15)

        self.appointments_last_30_days_label = ttk.Label(self.lblframe_customer_history,text="Reservations (Last 30 days)")
        self.appointments_last_30_days_entry = ttk.Entry(self.lblframe_customer_history, textvariable=self.appointments_last_30_days_var, state="readonly", width=15)

        self.appointments_last_7_days_label = ttk.Label(self.lblframe_customer_history, text="Reservations (Last 7 days)")
        self.appointments_last_7_days_entry = ttk.Entry(self.lblframe_customer_history, textvariable=self.appointments_last_7_days_var, state="readonly", width=15)

        self.appointments_all_time_label.grid(row=2, column=2, padx=(2, 2), pady=5, sticky="w")
        self.appointments_all_time_entry.grid(row=2, column=3, padx=(2, 2), pady=5, sticky="w")

        self.appointments_last_30_days_label.grid(row=3, column=2, padx=(2, 2), pady=5, sticky="w")
        self.appointments_last_30_days_entry.grid(row=3, column=3, padx=(2, 2), pady=5, sticky="w")

        self.appointments_last_7_days_label.grid(row=4, column=2, padx=(2, 2), pady=5, sticky="w")
        self.appointments_last_7_days_entry.grid(row=4, column=3, padx=(2, 2), pady=5, sticky="w")

    def populate_customers(self):
        customers = self.db.get_existing_customers()
        customers_sorted = sorted(customers, key=lambda c: c['FirstName'])
        menu = self.customer_menu["menu"]
        menu.delete(0, "end")

        for customer in customers_sorted:
            customer_fullname = f"{customer['FirstName']} {customer['LastName']}"
            self.customer_map[customer['CustomerID']] = customer_fullname
            menu.add_command(label=customer_fullname, command=lambda value=customer['CustomerID']: self.on_customer_selected(value))

    def on_customer_selected(self, customer_id):
        self.selected_customer_id = customer_id
        full_name = self.customer_map[customer_id]
        self.selected_customer_var.set(full_name)
        self.populate_customer_appointments()

        # Populate money spent
        money_spent = self.db.get_customer_money_spent(customer_id)
        self.spent_all_time_var.set(f"{money_spent['total_spent']:.2f}")
        self.spent_last_30_days_var.set(f"{money_spent['last_30_days_spent']:.2f}")
        self.spent_last_7_days_var.set(f"{money_spent['last_7_days_spent']:.2f}")

        # Populate appointment counts
        appointment_counts = self.db.get_customer_appointment_counts(customer_id)
        self.appointments_all_time_var.set(f"{appointment_counts['total_appointments']}")
        self.appointments_last_30_days_var.set(f"{appointment_counts['last_30_days_appointments']}")
        self.appointments_last_7_days_var.set(f"{appointment_counts['last_7_days_appointments']}")

    def populate_customer_appointments(self, *args):
        if self.selected_customer_id:
            results = self.db.get_customer_appointments(self.selected_customer_id)
            self.display_results(results)

    def populate_money_spent(self):
        if self.selected_customer_id:
            money_spent = self.db.get_customer_money_spent(self.selected_customer_id)
            self.spent_all_time_var.set(f"{money_spent['total_spent']:.2f}")
            self.spent_last_30_days_var.set(f"{money_spent['last_30_days_spent']:.2f}")
            self.spent_last_7_days_var.set(f"{money_spent['last_7_days_spent']:.2f}")

    def display_results(self, results):
        self.tree.delete(*self.tree.get_children())

        if results:
            for result in results:
                row = (f"{result.get('EmployeeFirstName', '')} {result.get('EmployeeLastName', '')}",
                       result.get("ServiceName", ""),
                       result.get("AppointmentDate", ""),
                       result.get("Status", ""),
                       result.get("Price", ""),
                       result.get("Notes", ""))
                self.tree.insert("", tk.END, values=row)
