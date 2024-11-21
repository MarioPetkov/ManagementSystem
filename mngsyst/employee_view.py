import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from person import Person
from mngsyst.error_handler import ErrorHandler


class EmployeeView:
    def __init__(self, notebook, db):
        self.notebook = notebook
        self.notebook = notebook
        self.db = db
        self.employee_id_to_update = None

        self.frame_employee = ttk.Frame(self.notebook)
        self.frame_employee.configure(height=200, padding=15, width=200)
        self.notebook.add(self.frame_employee, text="Employees")

        self.widgets_add_employee()
        self.widgets_edit_employee()
        self.widgets_employees_list()
        self.check_past_scheduled_appointments()


    def widgets_add_employee(self):
        self.lblframe_add_employee = ttk.Labelframe(self.frame_employee, text='Add employee')
        self.lblframe_add_employee.configure(height=200, padding=10, width=200)

        self.lbl_f_name = ttk.Label(self.lblframe_add_employee, text='Name*')
        self.lbl_l_name = ttk.Label(self.lblframe_add_employee, text='Surname*')
        self.lbl_phone_num = ttk.Label(self.lblframe_add_employee, text='Phone')
        self.lbl_position = ttk.Label(self.lblframe_add_employee, text='Position')
        self.lbl_age = ttk.Label(self.lblframe_add_employee, text='Age')
        self.lbl_gender = ttk.Label(self.lblframe_add_employee, text='Sex')
        self.lbl_start_date = ttk.Label(self.lblframe_add_employee, text='Start date*:')
        self.lbl_end_date = ttk.Label(self.lblframe_add_employee, text='End date:')

        self.entry_f_name = ttk.Entry(self.lblframe_add_employee)
        self.entry_l_name = ttk.Entry(self.lblframe_add_employee)
        self.entry_phone_num = ttk.Entry(self.lblframe_add_employee)
        self.entry_position = ttk.Entry(self.lblframe_add_employee)
        self.entry_age = ttk.Entry(self.lblframe_add_employee)
        self.entry_start_date = DateEntry(self.lblframe_add_employee, width=19, background='darkblue',
                                          foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_end_date = DateEntry(self.lblframe_add_employee, width=19, background='darkblue', foreground='white',
                                        borderwidth=2, date_pattern="dd-mm-yyyy")

        #self.entry_start_date.delete(0, "end")
        self.entry_start_date.set_date(datetime.date(1990, 1, 1))
        self.entry_end_date.set_date(datetime.date(2099, 12, 31))

        self.__add_selected_gender = tk.StringVar(value='Woman')
        self.optionmenu_gender = ttk.OptionMenu(self.lblframe_add_employee, self.__add_selected_gender, 'Woman',
                                                *Person.genders)

        self.btn_add_employee = ttk.Button(self.lblframe_add_employee, text='Add',
                                           command=self.add_employee_clicked)

        self.lbl_f_name.grid(column=0, row=0, sticky="e", **Person.padding)
        self.lbl_l_name.grid(column=0, row=1, sticky="e", **Person.padding)
        self.lbl_phone_num.grid(column=0, row=2, sticky="e", **Person.padding)
        self.lbl_age.grid(column=0, row=3, sticky="e", **Person.padding)
        self.lbl_position.grid(column=2, row=0, sticky="e", **Person.padding)
        self.lbl_gender.grid(column=2, row=3, sticky="e", **Person.padding)
        self.lbl_start_date.grid(column=2, row=1, sticky="e", **Person.padding)
        self.lbl_end_date.grid(column=2, row=2, sticky="e", **Person.padding)

        self.entry_f_name.grid(column=1, row=0, sticky="w", **Person.padding)
        self.entry_l_name.grid(column=1, row=1, sticky="w", **Person.padding)
        self.entry_phone_num.grid(column=1, row=2, sticky="w", **Person.padding)
        self.entry_age.grid(column=1, row=3, sticky="w", **Person.padding)
        self.entry_position.grid(column=3, row=0, sticky="w", **Person.padding)
        self.entry_start_date.grid(column=3, row=1, sticky="w", **Person.padding)
        self.entry_end_date.grid(column=3, row=2, sticky="w", **Person.padding)
        self.optionmenu_gender.grid(column=3, row=3, sticky="ew", **Person.padding)
        self.btn_add_employee.grid(column=0, columnspan=4, row=4, sticky="ew", **Person.padding)

        self.lblframe_add_employee.grid(column=0, row=0, sticky="nsew", **Person.padding)

    def widgets_edit_employee(self):
        self.lblframe_edit_employee = ttk.Labelframe(self.frame_employee, text='Edit')
        self.lblframe_edit_employee.configure(height=200, padding=10, width=200)

        self.lbl_edit_f_name = ttk.Label(self.lblframe_edit_employee, text='Name*')
        self.lbl_edit_l_name = ttk.Label(self.lblframe_edit_employee, text='Surname*')
        self.lbl_edit_phone_num = ttk.Label(self.lblframe_edit_employee, text='Phone')
        self.lbl_edit_position = ttk.Label(self.lblframe_edit_employee, text='Position')
        self.lbl_edit_age = ttk.Label(self.lblframe_edit_employee, text='Age')
        self.lbl_edit_gender = ttk.Label(self.lblframe_edit_employee, text='Sex')
        self.lbl_edit_start_date = ttk.Label(self.lblframe_edit_employee, text='Start date*:')
        self.lbl_edit_end_date = ttk.Label(self.lblframe_edit_employee, text='End date:')

        self.entry_edit_f_name = ttk.Entry(self.lblframe_edit_employee)
        self.entry_edit_l_name = ttk.Entry(self.lblframe_edit_employee)
        self.entry_edit_phone_num = ttk.Entry(self.lblframe_edit_employee)
        self.entry_edit_position = ttk.Entry(self.lblframe_edit_employee)
        self.entry_edit_age = ttk.Entry(self.lblframe_edit_employee)
        self.entry_edit_start_date = DateEntry(self.lblframe_edit_employee, width=19, background='darkblue',
                                               foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_edit_end_date = DateEntry(self.lblframe_edit_employee, width=19, background='darkblue',
                                             foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_edit_start_date.set_date(datetime.date(1990, 1, 1))
        self.entry_edit_end_date.set_date(datetime.date(2099, 12, 31))

        self.__edit_selected_gender = tk.StringVar()
        self.optionmenu_edit_gender = ttk.OptionMenu(self.lblframe_edit_employee, self.__edit_selected_gender, None,
                                                     *Person.genders)

        self.btn_update_employee = ttk.Button(self.lblframe_edit_employee, text='Edit',
                                              command=self.edit_employee_clicked)
        self.btn_delete_employee = ttk.Button(self.lblframe_edit_employee, text='Delete',
                                              command=self.delete_employee_clicked)

        self.lbl_edit_f_name.grid(column=0, row=0, sticky="e", **Person.padding)
        self.lbl_edit_l_name.grid(column=0, row=1, sticky="e", **Person.padding)
        self.lbl_edit_phone_num.grid(column=0, row=2, sticky="e", **Person.padding)
        self.lbl_edit_age.grid(column=0, row=3, sticky="e", **Person.padding)
        self.lbl_edit_position.grid(column=2, row=0, sticky="e", **Person.padding)
        self.lbl_edit_gender.grid(column=2, row=3, sticky="e", **Person.padding)
        self.lbl_edit_start_date.grid(column=2, row=1, sticky="e", **Person.padding)
        self.lbl_edit_end_date.grid(column=2, row=2, sticky="e", **Person.padding)

        self.entry_edit_f_name.grid(column=1, row=0, sticky="w", **Person.padding)
        self.entry_edit_l_name.grid(column=1, row=1, sticky="w", **Person.padding)
        self.entry_edit_phone_num.grid(column=1, row=2, sticky="w", **Person.padding)
        self.entry_edit_age.grid(column=1, row=3, sticky="w", **Person.padding)
        self.entry_edit_position.grid(column=3, row=0, sticky="w", **Person.padding)
        self.entry_edit_start_date.grid(column=3, row=1, sticky="w", **Person.padding)
        self.entry_edit_end_date.grid(column=3, row=2, sticky="w", **Person.padding)
        self.optionmenu_edit_gender.grid(column=3, row=3, sticky="ew", **Person.padding)
        self.btn_update_employee.grid(column=0, columnspan=4, row=4, sticky="ew", **Person.padding)
        self.btn_delete_employee.grid(column=0, columnspan=4, row=5, sticky="ew", **Person.padding)

        self.lblframe_edit_employee.grid(column=0, row=1, sticky="nsew", **Person.padding)

    def widgets_employees_list(self):
        self.lblframe_employees_list = ttk.Labelframe(self.frame_employee, text='Search:')
        self.lblframe_employees_list.configure(height=200, width=200)

        self.employee_tree = ttk.Treeview(self.lblframe_employees_list, columns=('EmployeeID', 'Name'), show='headings', height=19)

        self.entry_search_employee = ttk.Entry(self.lblframe_employees_list, width=23)
        self.entry_search_employee.bind("<KeyRelease>", self.search_employees)
        self.entry_search_employee.grid(column=0, row=0, sticky="ew", padx=5, pady=5)

        self.employee_tree.heading('EmployeeID', text='№')
        self.employee_tree.heading('Name', text='List of employees:')

        self.employee_tree.column('EmployeeID', minwidth=0, width=20, stretch=False)
        self.employee_tree.column('Name', minwidth=0, width=100, stretch=True)

        self.scrollbar = tk.Scrollbar(self.lblframe_employees_list, orient="vertical", command=self.employee_tree.yview)
        self.employee_tree.config(yscrollcommand=self.scrollbar.set)

        self.employee_tree.grid(column=0, row=1, sticky="nsew", **Person.padding)
        self.scrollbar.grid(column=1, row=1, sticky="ns", **Person.padding)
        self.lblframe_employees_list.grid(column=1, row=0, rowspan=3, sticky="nsw", **Person.padding)

        self.employee_tree.bind("<Double-1>", self.fill_employee_entries)

        self.populate_existing_employees()

    def fill_employee_entries(self, event):
        selected = self.employee_tree.focus()
        if selected:
            employee_id = self.employee_tree.item(selected)['values'][0]
            employee_info = self.db.get_employee_info(employee_id)

            self.entry_edit_f_name.delete(0, tk.END)
            self.entry_edit_f_name.insert(0, Person.get_valid_string(employee_info.get('FirstName', '')))

            self.entry_edit_l_name.delete(0, tk.END)
            self.entry_edit_l_name.insert(0, Person.get_valid_string(employee_info.get('LastName', '')))

            self.entry_edit_phone_num.delete(0, tk.END)
            self.entry_edit_phone_num.insert(0, Person.get_valid_string(employee_info.get('PhoneNumber', '')))

            self.entry_edit_position.delete(0, tk.END)
            self.entry_edit_position.insert(0, Person.get_valid_string(employee_info.get('Position', '')))

            self.entry_edit_age.delete(0, tk.END)
            self.entry_edit_age.insert(0, Person.get_valid_int(employee_info.get('Age', '')))

            self.__edit_selected_gender.set(Person.get_valid_string(employee_info.get('Gender', '')))

            start_date = Person.get_valid_date(employee_info.get('StartDate'))
            if start_date:
                self.entry_edit_start_date.set_date(start_date)
            else:
                self.entry_edit_start_date.set_date(datetime.date(1990, 1, 1))

            end_date = Person.get_valid_date(employee_info.get('EndDate'))
            if end_date:
                self.entry_edit_end_date.set_date(end_date)
            else:
                self.entry_edit_end_date.set_date(datetime.date(2099, 12, 31))

            self.employee_id_to_update = employee_id

    def populate_existing_employees(self):
        employees = self.db.get_existing_employees()
        self.employee_tree.delete(*self.employee_tree.get_children())

        for employee in employees:
            employee_id = employee['EmployeeID']
            name = f"{employee['FirstName']} {employee['LastName']}"
            self.employee_tree.insert('', 'end', values=(employee_id, name))

    def add_employee_clicked(self):
        entry_fields = [
            self.entry_f_name, self.entry_l_name, self.entry_phone_num,
            self.entry_age, self.entry_position, self.entry_start_date, self.entry_end_date
        ]
        option_menus = [self.__add_selected_gender]
        values = Person.get_person_data(entry_fields, option_menus)

        try:
            Person.check_provided_names(self.entry_f_name, self.entry_l_name)
            self.db.save_employee(values)
            Person.clear_input_fields(entry_fields, option_menus)
            self.populate_existing_employees()
            ErrorHandler.show_info("Added", "Successfully added employee!")
        except Exception as e:
            ErrorHandler.show_error("Error", f"Error occured: {e}")

    def edit_employee_clicked(self):
        if not self.employee_id_to_update:
            ErrorHandler.show_warning("Edit", "Choose employee to edit!")
            return

        entry_fields = [
            self.entry_edit_f_name, self.entry_edit_l_name, self.entry_edit_phone_num,
            self.entry_edit_age, self.entry_edit_position, self.entry_edit_start_date, self.entry_edit_end_date
        ]
        option_menus = [self.__edit_selected_gender]
        values = Person.get_person_data(entry_fields, option_menus)

        try:
            self.db.update_employee(values, self.employee_id_to_update)
            Person.clear_input_fields(entry_fields, option_menus)
            self.populate_existing_employees()
            ErrorHandler.show_info("Edited", "Successfully edited employee!")
        except Exception as e:
            ErrorHandler.show_error("Error", f"Error occured: {e}")

    def delete_employee_clicked(self):
        if not self.employee_id_to_update:
            ErrorHandler.show_warning("Delete", "Please choose an employee to delete!")
            return

        entry_fields = [
            self.entry_edit_f_name, self.entry_edit_l_name, self.entry_edit_phone_num,
            self.entry_edit_age, self.entry_edit_position, self.entry_edit_start_date, self.entry_edit_end_date
        ]
        option_menus = [self.__edit_selected_gender]

        try:
            self.db.delete_employee(self.employee_id_to_update)
            Person.clear_input_fields(entry_fields, option_menus)
            self.populate_existing_employees()
            ErrorHandler.show_info("Deleted", "The Employee is deleted!")
            self.employee_id_to_update = None
        except Exception as e:
            ErrorHandler.show_error("Error", f"Error occured: {e}")

    def search_employees(self, event):
        search_term = self.entry_search_employee.get().strip().lower()
        self.employee_tree.delete(*self.employee_tree.get_children())  # Clear existing entries

        if not search_term:
            self.populate_existing_employees()
        else:
            employees = self.db.search_employees(search_term)
            for employee in employees:
                employee_id = employee['EmployeeID']
                name = f"{employee['FirstName']} {employee['LastName']}"
                self.employee_tree.insert('', 'end', values=(employee_id, name))

    def check_past_scheduled_appointments(self):
        past_appointments = self.db.get_past_scheduled_appointments()

        for appointment in past_appointments:
            appointment_id = appointment['AppointmentID']
            customer_name = f"{appointment['CustomerFirstName']} {appointment['CustomerLastName']}"
            appointment_date = appointment['AppointmentDate']

            # Ask the user to change the status
            new_status = self.ask_status_change(customer_name, appointment_date)
            if new_status:
                self.db.update_appointment_status(appointment_id, new_status.capitalize())

    def ask_status_change(self, customer_name, appointment_date):
        window = tk.Toplevel(self.frame_employee)
        window.title("Current status on past appointment")

        # Make the window modal
        window.grab_set()

        # Set the size of the popup window
        window_width = 300
        window_height = 100

        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the position to center the window
        position_x = int((screen_width / 2) - (window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        # Set the window geometry to center it
        window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        window.attributes('-topmost', True)

        # Wrap the text if it exceeds the window width
        label_text = f"Change status on {customer_name} for {appointment_date}:"
        label = tk.Label(window, text=label_text, wraplength=window_width - 40)
        label.pack(padx=20, pady=10)

        status_var = tk.StringVar()

        btn_completed = tk.Button(window, text="Successfull",
                                  command=lambda: self.set_status_and_close(window, status_var, "Sucessfull"))
        btn_canceled = tk.Button(window, text="Cancelled",
                                 command=lambda: self.set_status_and_close(window, status_var, "Cancelled"))

        btn_completed.pack(side=tk.LEFT, padx=20, pady=10)
        btn_canceled.pack(side=tk.RIGHT, padx=20, pady=10)

        window.wait_window()  # Wait for the window to close

        return status_var.get()

    def set_status_and_close(self, window, status_var, status):
        status_var.set(status)
        window.destroy()