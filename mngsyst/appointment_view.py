import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from mngsyst.error_handler import ErrorHandler

from person import Person


class AppointmentView:
    def __init__(self, notebook, db):
        self.notebook = notebook
        self.db = db
        self.appointment_id_to_update = None
        self.opt_mnu_width = 10

        self.frame_appointment = ttk.Frame(self.notebook)
        self.frame_appointment.configure(height=200, padding=15, width=200)
        self.notebook.add(self.frame_appointment, text="Reservation")

        self.widgets_add_appointment()
        self.widgets_edit_appointment()
        self.widgets_appointment_list()

    def widgets_add_appointment(self):
        self.lblframe_add_appointment = ttk.Labelframe(self.frame_appointment, text='Add reservation')
        self.lblframe_add_appointment.configure(height=200, padding=10, width=200)

        self.lbl_for_employee = ttk.Label(self.lblframe_add_appointment, text='Employee*')
        self.lbl_for_customer = ttk.Label(self.lblframe_add_appointment, text='Customer*')
        self.lbl_for_service = ttk.Label(self.lblframe_add_appointment, text='Service*')
        self.lbl_appointment_date = ttk.Label(self.lblframe_add_appointment, text='Date*')
        self.lbl_status = ttk.Label(self.lblframe_add_appointment, text='Status*')
        self.lbl_notes = ttk.Label(self.lblframe_add_appointment, text='Note')

        employees = self.db.get_existing_employees()
        self.employee_options = {f"{emp['FirstName']} {emp['LastName']}": emp['EmployeeID'] for emp in employees}
        self.__add_selected_employee = tk.StringVar()
        self.optionmenu_for_employee = ttk.OptionMenu(self.lblframe_add_appointment, self.__add_selected_employee, None,
                                                      *self.employee_options.keys())
        self.optionmenu_for_employee.configure(width=self.opt_mnu_width)

        customers = self.db.get_existing_customers()
        self.customer_options = {f"{cust['FirstName']} {cust['LastName']}": cust['CustomerID'] for cust in customers}
        self.__add_selected_customer = tk.StringVar()
        self.optionmenu_for_customer = ttk.OptionMenu(self.lblframe_add_appointment, self.__add_selected_customer, None,
                                                      *self.customer_options.keys())
        self.optionmenu_for_customer.configure(width=self.opt_mnu_width)

        services = self.db.get_existing_services()
        self.service_options = {f"{serv['ServiceName']}": serv['ServiceID'] for serv in services}
        self.__add_selected_service = tk.StringVar()
        self.optionmenu_for_service = ttk.OptionMenu(self.lblframe_add_appointment, self.__add_selected_service, None,
                                                     *self.service_options.keys())
        self.optionmenu_for_service.configure(width=self.opt_mnu_width)

        self.entry_appointment_date = DateEntry(self.lblframe_add_appointment, width=19, background='darkblue',
                                                foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_appointment_date.configure(width=13)

        self.__add_selected_status = tk.StringVar(value='Appointed')
        self.optionmenu_status = ttk.OptionMenu(self.lblframe_add_appointment, self.__add_selected_status, 'Appointed',
                                                *Person.status)
        self.optionmenu_status.configure(width=self.opt_mnu_width)

        self.entry_notes = ttk.Entry(self.lblframe_add_appointment)
        self.entry_notes.configure(width=14)

        self.btn_add_appointment = ttk.Button(self.lblframe_add_appointment, text='Save',
                                              command=self.add_appointment_clicked)

        self.lbl_for_employee.grid(column=0, row=0, sticky="e", **Person.padding)
        self.optionmenu_for_employee.grid(column=1, row=0, sticky="w", **Person.padding)

        self.lbl_for_customer.grid(column=0, row=1, sticky="e", **Person.padding)
        self.optionmenu_for_customer.grid(column=1, row=1, sticky="w", **Person.padding)

        self.lbl_for_service.grid(column=0, row=2, sticky="e", **Person.padding)
        self.optionmenu_for_service.grid(column=1, row=2, sticky="w", **Person.padding)

        self.lbl_appointment_date.grid(column=2, row=0, sticky="e", **Person.padding)
        self.entry_appointment_date.grid(column=3, row=0, sticky="w", **Person.padding)

        self.lbl_status.grid(column=2, row=1, sticky="e", **Person.padding)
        self.optionmenu_status.grid(column=3, row=1, sticky="w", **Person.padding)

        self.lbl_notes.grid(column=2, row=2, sticky="e", **Person.padding)
        self.entry_notes.grid(column=3, row=2, sticky="w", **Person.padding)

        self.btn_add_appointment.grid(column=0, columnspan=4, row=3, sticky="ew", **Person.padding)

        self.lblframe_add_appointment.grid(column=0, row=0, sticky="nsew", **Person.padding)

    def widgets_edit_appointment(self):
        self.lblframe_edit_appointment = ttk.Labelframe(self.frame_appointment, text='Edit')
        self.lblframe_edit_appointment.configure(height=200, padding=10, width=200)

        self.lbl_edit_employee = ttk.Label(self.lblframe_edit_appointment, text='Employee*')
        self.lbl_edit_customer = ttk.Label(self.lblframe_edit_appointment, text='Customer*')
        self.lbl_edit_service = ttk.Label(self.lblframe_edit_appointment, text='Service*')
        self.lbl_edit_appointment_date = ttk.Label(self.lblframe_edit_appointment, text='Date*')
        self.lbl_edit_status = ttk.Label(self.lblframe_edit_appointment, text='Status*')
        self.lbl_edit_notes = ttk.Label(self.lblframe_edit_appointment, text='Note')

        self.__edit_selected_employee = tk.StringVar()
        self.optionmenu_edit_employee = ttk.OptionMenu(self.lblframe_edit_appointment, self.__edit_selected_employee, None,
                                                       *self.employee_options.keys())
        self.optionmenu_edit_employee.configure(width=self.opt_mnu_width)


        self.__edit_selected_customer = tk.StringVar()
        self.optionmenu_edit_customer = ttk.OptionMenu(self.lblframe_edit_appointment, self.__edit_selected_customer, None,
                                                       *self.customer_options.keys())
        self.optionmenu_edit_customer.configure(width=self.opt_mnu_width)

        self.__edit_selected_service = tk.StringVar()
        self.optionmenu_edit_service = ttk.OptionMenu(self.lblframe_edit_appointment, self.__edit_selected_service, None,
                                                      *self.service_options.keys())
        self.optionmenu_edit_service.configure(width=self.opt_mnu_width)

        self.entry_edit_appointment_date = DateEntry(self.lblframe_edit_appointment, width=19, background='darkblue',
                                                     foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_edit_appointment_date.configure(width=13)

        self.__edit_selected_status = tk.StringVar()
        self.optionmenu_edit_status = ttk.OptionMenu(self.lblframe_edit_appointment, self.__edit_selected_status, None,
                                                     *Person.status)
        self.optionmenu_edit_status.configure(width=self.opt_mnu_width)

        self.entry_edit_notes = ttk.Entry(self.lblframe_edit_appointment)
        self.entry_edit_notes.configure(width=14)

        self.btn_update_appointment = ttk.Button(self.lblframe_edit_appointment, text='Edit',
                                                 command=self.edit_appointment_clicked)
        self.btn_delete_appointment = ttk.Button(self.lblframe_edit_appointment, text='Delete',
                                                 command=self.delete_appointment_clicked)

        self.lbl_edit_employee.grid(column=0, row=0, sticky="e", **Person.padding)
        self.optionmenu_edit_employee.grid(column=1, row=0, sticky="w", **Person.padding)

        self.lbl_edit_customer.grid(column=0, row=1, sticky="e", **Person.padding)
        self.optionmenu_edit_customer.grid(column=1, row=1, sticky="w", **Person.padding)

        self.lbl_edit_service.grid(column=0, row=2, sticky="e", **Person.padding)
        self.optionmenu_edit_service.grid(column=1, row=2, sticky="w", **Person.padding)

        self.lbl_edit_appointment_date.grid(column=2, row=0, sticky="e", **Person.padding)
        self.entry_edit_appointment_date.grid(column=3, row=0, sticky="w", **Person.padding)

        self.lbl_edit_status.grid(column=2, row=1, sticky="e", **Person.padding)
        self.optionmenu_edit_status.grid(column=3, row=1, sticky="w", **Person.padding)

        self.lbl_edit_notes.grid(column=2, row=2, sticky="e", **Person.padding)
        self.entry_edit_notes.grid(column=3, row=2, sticky="w", **Person.padding)

        self.btn_update_appointment.grid(column=0, columnspan=4, row=3, sticky="ew", **Person.padding)
        self.btn_delete_appointment.grid(column=0, columnspan=4, row=4, sticky="ew", **Person.padding)

        self.lblframe_edit_appointment.grid(column=0, row=1, sticky="nsew", **Person.padding)

    def widgets_appointment_list(self):
        self.lblframe_appointments_list = ttk.Labelframe(self.frame_appointment, text='Search:')
        self.lblframe_appointments_list.configure(height=200, width=200)

        self.appointment_tree = ttk.Treeview(self.lblframe_appointments_list, columns=('AppointmentID', 'Employee', 'Customer', 'Service', 'Date', 'Status'), show='headings', height=19)

        self.entry_search_appointment = ttk.Entry(self.lblframe_appointments_list, width=20)
        self.entry_search_appointment.bind("<KeyRelease>", self.search_appointments)
        self.entry_search_appointment.grid(column=0, row=0, sticky="ew", padx=5, pady=5)

        self.appointment_tree.heading('AppointmentID', text='№')
        self.appointment_tree.heading('Employee', text='Employee')
        self.appointment_tree.heading('Customer', text='Customer')
        self.appointment_tree.heading('Service', text='Service')
        self.appointment_tree.heading('Date', text='Date')
        self.appointment_tree.heading('Status', text='Status')

        self.appointment_tree.column('AppointmentID', minwidth=0, width=20, stretch=False)
        self.appointment_tree.column('Employee', minwidth=0, width=120, stretch=False)
        self.appointment_tree.column('Customer', minwidth=0, width=120, stretch=False)
        self.appointment_tree.column('Service', minwidth=0, width=120, stretch=False)
        self.appointment_tree.column('Date', minwidth=0, width=90, stretch=False)
        self.appointment_tree.column('Status', minwidth=0, width=80, stretch=False)

        yscrollbar = tk.Scrollbar(self.lblframe_appointments_list, orient="vertical", command=self.appointment_tree.yview)
        self.appointment_tree.config(yscrollcommand=yscrollbar.set)

        xscrollbar = tk.Scrollbar(self.lblframe_appointments_list, orient="horizontal", command=self.appointment_tree.xview)
        self.appointment_tree.config(xscrollcommand=xscrollbar.set)

        self.appointment_tree.grid(column=0, row=1, sticky="nsew", **Person.padding)
        yscrollbar.grid(column=1, row=2, sticky="ns", **Person.padding)
        xscrollbar.grid(column=1, row=2, sticky="ew", **Person.padding)
        self.lblframe_appointments_list.grid(column=1, row=0, rowspan=2, sticky="nsew")
        self.appointment_tree.bind('<Double-1>', self.fill_appointment_entries)

        self.populate_existing_appointments()


    def populate_existing_appointments(self):
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)

        appointments = self.db.get_existing_appointments()
        for appointment in appointments:
            employee = f"{appointment['EmployeeFirstName']} {appointment['EmployeeLastName']}"
            customer = f"{appointment['CustomerFirstName']} {appointment['CustomerLastName']}"
            service = appointment['ServiceName']
            date = appointment['AppointmentDate']
            status = appointment['Status']

            self.appointment_tree.insert('', tk.END, values=(
            appointment['AppointmentID'], employee, customer, service, date, status))

    def add_appointment_clicked(self):
        employee_name = self.__add_selected_employee.get()
        customer_name = self.__add_selected_customer.get()
        service_name = self.__add_selected_service.get()
        date = self.entry_appointment_date.get_date()

        formatted_date = date.strftime('%Y-%m-%d')

        status = self.__add_selected_status.get()
        notes = self.entry_notes.get()

        if not employee_name or not customer_name or not service_name or not formatted_date:
            ErrorHandler.show_error("Error", "Fulfill the mandatory fields!")
            return

        entry_fields = [
            self.entry_appointment_date, self.entry_notes
        ]
        option_menus = [self.__add_selected_employee, self.__add_selected_customer, self.__add_selected_service, self.__add_selected_status]
        values = Person.get_person_data(entry_fields, option_menus)

        employee_id = self.employee_options.get(employee_name)
        customer_id = self.customer_options.get(customer_name)
        service_id = self.service_options.get(service_name)
        try:
            self.db.save_appointment(employee_id, customer_id, service_id, formatted_date, status, notes)
            Person.clear_input_fields(entry_fields, option_menus)
            self.populate_existing_appointments()
            ErrorHandler.show_info("Appointed", "Successfully appointed")
        except Exception as e:
            ErrorHandler.show_error("Add appointemnt", f"Error occured: {e}")
    def edit_appointment_clicked(self):
        if not self.appointment_id_to_update:
            ErrorHandler.show_warning("Edit", "Please choose appointment to edit!")
            return

        employee_name = self.__edit_selected_employee.get()
        customer_name = self.__edit_selected_customer.get()
        service_name = self.__edit_selected_service.get()
        date = self.entry_edit_appointment_date.get_date()
        status = self.__edit_selected_status.get()
        notes = self.entry_edit_notes.get()

        formatted_date = date.strftime('%Y-%m-%d')

        if not employee_name or not customer_name or not service_name or not formatted_date:
            ErrorHandler.show_error("Error", "Fulfill the mandatory fields!")
            return

        entry_fields = [
            self.entry_edit_appointment_date, self.entry_edit_notes
        ]
        option_menus = [self.__edit_selected_employee, self.__edit_selected_customer, self.__edit_selected_service,
                        self.__edit_selected_status]
        values = Person.get_person_data(entry_fields, option_menus)

        employee_id = self.employee_options.get(employee_name)
        customer_id = self.customer_options.get(customer_name)
        service_id = self.service_options.get(service_name)
        try:
            self.db.update_appointment(self.appointment_id_to_update, employee_id, customer_id, service_id, date, status, notes)
            Person.clear_input_fields(entry_fields, option_menus)
            self.populate_existing_appointments()
            ErrorHandler.show_info("Edited", "Successfully edited appointment.")
        except Exception as e:
            ErrorHandler.show_error("Error", f"Error occured: {e}")

    def delete_appointment_clicked(self):
        if self.appointment_id_to_update is None:
            ErrorHandler.show_warning("Delete", "Choose appointment to delete.")
            return
        entry_fields = [
            self.entry_edit_appointment_date, self.entry_edit_notes
        ]
        option_menus = [self.__edit_selected_employee, self.__edit_selected_customer, self.__edit_selected_service,
                        self.__edit_selected_status]

        try:
            messagebox.askyesno("Delete Appointment", "Please confirm you want to delete the appointment!")
            self.db.delete_appointment(self.appointment_id_to_update)
            Person.clear_input_fields(entry_fields, option_menus)
            ErrorHandler.show_info("Successfully deleted", "Successfully deleted apointment")
            self.populate_existing_appointments()
        except Exception as e:
            ErrorHandler.show_error("Error occured", f"Error occured: {e}")



    def fill_appointment_entries(self, event):
        selected = self.appointment_tree.focus()
        try:
            values = self.appointment_tree.item(selected, 'values')
            appointment_id = values[0]
            self.appointment_id_to_update = appointment_id

            employee_name = values[1]
            customer_name = values[2]
            service_name = values[3]
            status = values[5]

            # Fetch the notes and any additional information from the database
            appointment_info = self.db.fetch_appointment_by_id(appointment_id)
            db_date = appointment_info.get('AppointmentDate')

            display_date = datetime.datetime.strptime(db_date, '%Y-%m-%d').strftime('%d-%m-%Y')

            self.entry_edit_appointment_date.set_date(display_date)
            notes = appointment_info.get('Notes', '')

            self.__edit_selected_employee.set(Person.get_valid_string(employee_name))
            self.__edit_selected_customer.set(Person.get_valid_string(customer_name))
            self.__edit_selected_service.set(Person.get_valid_string(service_name))
            self.__edit_selected_status.set(Person.get_valid_string(status))
            self.entry_edit_notes.delete(0, tk.END)
            self.entry_edit_notes.insert(0, notes)

            # app_date = Person.get_valid_date(date)
            if display_date:
                self.entry_edit_appointment_date.set_date(display_date)
            else:
                self.entry_edit_appointment_date.set_date(datetime.date(1990, 1, 1))

        except Exception as e:
            ErrorHandler.show_error("Error filling", f"Error occured: {e}")

    def search_appointments(self, event):
        search_term = self.entry_search_appointment.get().strip().lower()
        self.appointment_tree.delete(*self.appointment_tree.get_children())  # Clear existing entries

        if not search_term:
            self.populate_existing_appointments()
        else:
            appointments = self.db.search_appointments(search_term)
            for appointment in appointments:
                try:
                    employee = f"{appointment['EmployeeFirstName']} {appointment['EmployeeLastName']}"
                    customer = f"{appointment['CustomerFirstName']} {appointment['CustomerLastName']}"
                    service = appointment['ServiceName']
                    date = appointment['AppointmentDate']
                    status = appointment['Status']

                    self.appointment_tree.insert('', 'end', values=(
                    appointment['AppointmentID'], employee, customer, service, date, status))
                except KeyError as e:
                    ErrorHandler.show_error("Missing key in appointment data", f"{e}")