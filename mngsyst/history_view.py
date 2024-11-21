import tkinter as tk
from tkinter import ttk


class AppointmentsHistory:
    def __init__(self, notebook, db):
        self.notebook = notebook
        self.db = db

        # Create the frame for the History tab
        self.frame_history = ttk.Frame(self.notebook)
        self.frame_history.configure(height=200, padding=15, width=200)
        self.notebook.add(self.frame_history, text="Report")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_history)  # Trace changes to the search field

        self.setup_ui()
        self.populate_all_appointments()

    def setup_ui(self):
        # Create the Labelframe to contain the search and display UI
        self.lblframe_history = ttk.Labelframe(self.frame_history, text="Report")
        self.lblframe_history.configure(padding=10)
        self.lblframe_history.grid(row=0, column=0, sticky="nsew")

        # Create widgets for search input
        self.search_label = tk.Label(self.lblframe_history, text="Search:")
        self.search_entry = tk.Entry(self.lblframe_history, width=40, textvariable=self.search_var)

        # Layout for the search bar
        self.search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry.grid(row=0, column=1, padx=(5, 20), pady=5, sticky="w")

        # Create readonly fields for displaying appointment counts
        self.total_label = tk.Label(self.lblframe_history, text="Reservations (Total):")
        self.total_entry = tk.Entry(self.lblframe_history, width=15, state='readonly')
        self.total_label.grid(row=2, column=0, padx=(5, 2), pady=5, sticky="w")
        self.total_entry.grid(row=2, column=1, padx=(2, 5), pady=5, sticky="w")

        self.last_30_days_label = tk.Label(self.lblframe_history, text="Reservations (Last 30 days):")
        self.last_30_days_entry = tk.Entry(self.lblframe_history, width=15, state='readonly')
        self.last_30_days_label.grid(row=3, column=0, padx=(5, 2), pady=5, sticky="w")
        self.last_30_days_entry.grid(row=3, column=1, padx=(2, 5), pady=5, sticky="w")

        self.last_7_days_label = tk.Label(self.lblframe_history, text="Reservations (Last 7 days):")
        self.last_7_days_entry = tk.Entry(self.lblframe_history, width=15, state='readonly')
        self.last_7_days_label.grid(row=4, column=0, padx=(5, 2), pady=5, sticky="w")
        self.last_7_days_entry.grid(row=4, column=1, padx=(2, 5), pady=5, sticky="w")

        # Create the Treeview widget for displaying the results
        self.tree = ttk.Treeview(self.lblframe_history, columns=("EmployeeFullName", "CustomerFullName",
                                                                 "ServiceName", "AppointmentDate",
                                                                 "Status", "Notes"),
                                 show='headings', height=12)

        # Define the column headings and widths
        self.tree.heading("EmployeeFullName", text="Employee")
        self.tree.heading("CustomerFullName", text="Customer")
        self.tree.heading("ServiceName", text="Service")
        self.tree.heading("AppointmentDate", text="Date")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Notes", text="Note")

        self.tree.column("EmployeeFullName", width=120)
        self.tree.column("CustomerFullName", width=120)
        self.tree.column("ServiceName", width=130)
        self.tree.column("AppointmentDate", width=100)
        self.tree.column("Status", width=100)
        self.tree.column("Notes", width=220)

        self.tree.grid(row=1, column=0, columnspan=8, padx=5, pady=5, sticky="nsew")

        # Add a vertical scrollbar to the Treeview
        self.scrollbar = ttk.Scrollbar(self.lblframe_history, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=8, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Ensure that the Treeview widget does not expand beyond the fixed window size
        self.lblframe_history.grid_columnconfigure(0, weight=1)
        self.lblframe_history.grid_rowconfigure(1, weight=1)

    def search_history(self, *args):
        search_term = self.search_var.get().strip()

        if search_term:
            search_terms = search_term.lower().split()
            search_term_combined = ' '.join(search_terms)
            results = self.db.search_appointments(search_term_combined)
            summary = self.db.count_appointments_summary(search_terms)
        else:
            results = self.db.fetch_all_appointments_ordered()
            summary = self.db.count_appointments_summary()

        self.display_results(results)
        self.update_appointment_counts(summary)

    def update_appointment_counts(self, summary):
        self.total_entry.config(state='normal')
        self.last_30_days_entry.config(state='normal')
        self.last_7_days_entry.config(state='normal')

        self.total_entry.delete(0, tk.END)
        self.total_entry.insert(0, summary['total_count'])
        self.last_30_days_entry.delete(0, tk.END)
        self.last_30_days_entry.insert(0, summary['last_30_days_count'])
        self.last_7_days_entry.delete(0, tk.END)
        self.last_7_days_entry.insert(0, summary['last_7_days_count'])

        self.total_entry.config(state='readonly')
        self.last_30_days_entry.config(state='readonly')
        self.last_7_days_entry.config(state='readonly')

    def display_results(self, results):
        self.tree.delete(*self.tree.get_children())

        if results:
            for result in results:
                row = (f"{result.get('EmployeeFirstName', '')} {result.get('EmployeeLastName', '')}",
                       f"{result.get('CustomerFirstName', '')} {result.get('CustomerLastName', '')}",
                       result.get("ServiceName", ""),
                       result.get("AppointmentDate", ""),
                       result.get("Status", ""),
                       result.get("Notes", ""))
                self.tree.insert("", tk.END, values=row)

    def populate_all_appointments(self):
        results = self.db.fetch_all_appointments_ordered()
        summary = self.db.count_appointments_summary()

        self.display_results(results)
        self.update_appointment_counts(summary)
