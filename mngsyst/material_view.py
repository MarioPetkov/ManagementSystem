import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from mngsyst.error_handler import ErrorHandler

from person import Person



class MaterialView:
    def __init__(self, notebook, db):
        self.notebook = notebook
        self.db = db
        self.material_id_to_update = None

        self.frame_material = ttk.Frame(self.notebook)
        self.frame_material.configure(height=200, padding=15, width=200)
        self.notebook.add(self.frame_material, text="Materials")

        self.widgets_add_material()
        self.widgets_edit_material()
        self.widgets_materials_list()

    def widgets_add_material(self):
        self.lblframe_add_material = ttk.Labelframe(self.frame_material, text='Add material')
        self.lblframe_add_material.configure(height=200, padding=10, width=200)


        self.lbl_name = ttk.Label(self.lblframe_add_material, text='Name*')
        self.lbl_type = ttk.Label(self.lblframe_add_material, text='Type')
        self.lbl_brand = ttk.Label(self.lblframe_add_material, text='Model*')
        self.lbl_price = ttk.Label(self.lblframe_add_material, text='Price*')
        self.lbl_open_date = ttk.Label(self.lblframe_add_material, text='Started:')
        self.lbl_finish_date = ttk.Label(self.lblframe_add_material, text='Finished:')
        self.lbl_for_employee = ttk.Label(self.lblframe_add_material, text='For employee*:')

        self.entry_name = ttk.Entry(self.lblframe_add_material)
        self.entry_type = ttk.Entry(self.lblframe_add_material)
        self.entry_brand = ttk.Entry(self.lblframe_add_material)
        self.entry_price = ttk.Entry(self.lblframe_add_material)
        self.entry_open_date = DateEntry(self.lblframe_add_material, width=19, background='darkblue',
                                         foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_finish_date = DateEntry(self.lblframe_add_material, width=19, background='darkblue',
                                           foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_open_date.set_date(datetime.date(1990, 1, 1))
        self.entry_finish_date.set_date(datetime.date(2099, 12, 31))

        employees = self.db.get_existing_employees()
        self.employee_options = {f"{emp['FirstName']} {emp['LastName']}": emp['EmployeeID'] for emp in employees}
        self.__add_selected_employee = tk.StringVar()
        self.optionmenu_for_employee = ttk.OptionMenu(self.lblframe_add_material, self.__add_selected_employee, None,
                                                      *self.employee_options.keys())

        self.btn_add_material = ttk.Button(self.lblframe_add_material, text='Add',
                                           command=self.add_material_clicked)

        self.lbl_name.grid(column=0, row=0, sticky="e", **Person.padding)
        self.lbl_type.grid(column=0, row=1, sticky="e", **Person.padding)
        self.lbl_brand.grid(column=0, row=2, sticky="e", **Person.padding)
        self.lbl_price.grid(column=0, row=3, sticky="e", **Person.padding)
        self.lbl_open_date.grid(column=2, row=0, sticky="e", **Person.padding)
        self.lbl_finish_date.grid(column=2, row=1, sticky="e", **Person.padding)
        self.lbl_for_employee.grid(column=2, row=2, sticky="e", **Person.padding)

        self.entry_name.grid(column=1, row=0, sticky="w", **Person.padding)
        self.entry_type.grid(column=1, row=1, sticky="w", **Person.padding)
        self.entry_brand.grid(column=1, row=2, sticky="w", **Person.padding)
        self.entry_price.grid(column=1, row=3, sticky="w", **Person.padding)
        self.entry_open_date.grid(column=3, row=0, sticky="w", **Person.padding)
        self.entry_finish_date.grid(column=3, row=1, sticky="w", **Person.padding)
        self.optionmenu_for_employee.grid(column=3, row=2, sticky="w", **Person.padding)
        self.btn_add_material.grid(column=0, columnspan=4, row=4, sticky="ew", **Person.padding)

        self.lblframe_add_material.grid(column=0, row=0, sticky="nsew", **Person.padding)

    def widgets_edit_material(self):
        self.lblframe_edit_material = ttk.Labelframe(self.frame_material, text='Edit')
        self.lblframe_edit_material.configure(height=200, padding=10, width=200)

        self.lbl_edit_name = ttk.Label(self.lblframe_edit_material, text='Name*')
        self.lbl_edit_type = ttk.Label(self.lblframe_edit_material, text='Type')
        self.lbl_edit_brand = ttk.Label(self.lblframe_edit_material, text='Model*')
        self.lbl_edit_price = ttk.Label(self.lblframe_edit_material, text='Price*')
        self.lbl_edit_open_date = ttk.Label(self.lblframe_edit_material, text='Started:')
        self.lbl_edit_finish_date = ttk.Label(self.lblframe_edit_material, text='Finished:')
        self.lbl_edit_for_employee = ttk.Label(self.lblframe_edit_material, text='For employee*:')

        self.entry_edit_name = ttk.Entry(self.lblframe_edit_material)
        self.entry_edit_type = ttk.Entry(self.lblframe_edit_material)
        self.entry_edit_brand = ttk.Entry(self.lblframe_edit_material)
        self.entry_edit_price = ttk.Entry(self.lblframe_edit_material)
        self.entry_edit_open_date = DateEntry(self.lblframe_edit_material, width=19, background='darkblue',
                                              foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_edit_finish_date = DateEntry(self.lblframe_edit_material, width=19, background='darkblue',
                                                foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
        self.entry_edit_open_date.set_date(datetime.date(1990, 1, 1))
        self.entry_edit_finish_date.set_date(datetime.date(2099, 12, 31))

        employees = self.db.get_existing_employees()
        self.edit_employee_options = {f"{emp['FirstName']} {emp['LastName']}": emp['EmployeeID'] for emp in employees}
        self.__edit_selected_employee = tk.StringVar()
        self.optionmenu_edit_for_employee = ttk.OptionMenu(self.lblframe_edit_material, self.__edit_selected_employee,
                                                           None, *self.edit_employee_options.keys())

        self.btn_edit_material = ttk.Button(self.lblframe_edit_material, text='Edit',
                                            command=self.edit_material_clicked)
        self.btn_delete_material = ttk.Button(self.lblframe_edit_material, text='Delete',
                                            command=self.delete_material_clicked)

        self.lbl_edit_name.grid(column=0, row=0, sticky="e", **Person.padding)
        self.lbl_edit_type.grid(column=0, row=1, sticky="e", **Person.padding)
        self.lbl_edit_brand.grid(column=0, row=2, sticky="e", **Person.padding)
        self.lbl_edit_price.grid(column=0, row=3, sticky="e", **Person.padding)
        self.lbl_edit_open_date.grid(column=2, row=0, sticky="e", **Person.padding)
        self.lbl_edit_finish_date.grid(column=2, row=1, sticky="e", **Person.padding)
        self.lbl_edit_for_employee.grid(column=2, row=2, sticky="e", **Person.padding)

        self.entry_edit_name.grid(column=1, row=0, sticky="w", **Person.padding)
        self.entry_edit_type.grid(column=1, row=1, sticky="w", **Person.padding)
        self.entry_edit_brand.grid(column=1, row=2, sticky="w", **Person.padding)
        self.entry_edit_price.grid(column=1, row=3, sticky="w", **Person.padding)
        self.entry_edit_open_date.grid(column=3, row=0, sticky="w", **Person.padding)
        self.entry_edit_finish_date.grid(column=3, row=1, sticky="w", **Person.padding)
        self.optionmenu_edit_for_employee.grid(column=3, row=2, sticky="w", **Person.padding)
        self.btn_edit_material.grid(column=0, columnspan=4, row=4, sticky="ew", **Person.padding)
        self.btn_delete_material.grid(column=0, columnspan=4, row=5, sticky="ew", **Person.padding)

        self.lblframe_edit_material.grid(column=0, row=1, sticky="nsew", **Person.padding)

    def widgets_materials_list(self):
        self.lblframe_materials_list = ttk.Labelframe(self.frame_material, text='Search:')
        self.lblframe_materials_list.configure(height=200, width=200)


        self.material_tree = ttk.Treeview(self.lblframe_materials_list, columns=('MaterialID', 'Name'), show='headings',
                                          height=19)

        self.entry_search_material = ttk.Entry(self.lblframe_materials_list, width=26)
        self.entry_search_material.bind("<KeyRelease>", self.search_material)
        self.entry_search_material.grid(column=0, row=0, sticky="ew", padx=5, pady=5)

        self.material_tree.heading('MaterialID', text='№')
        self.material_tree.heading('Name', text='List of materials')

        self.material_tree.column('MaterialID', minwidth=0, width=30, stretch=False)
        self.material_tree.column('Name', minwidth=0, width=100, stretch=True)

        self.scrollbar = tk.Scrollbar(self.lblframe_materials_list, orient="vertical", command=self.material_tree.yview)
        self.material_tree.config(yscrollcommand=self.scrollbar.set)

        self.material_tree.grid(column=0, row=1, sticky="nsew", **Person.padding)
        self.scrollbar.grid(column=1, row=1, sticky="ns", **Person.padding)
        self.lblframe_materials_list.grid(column=1, row=0, rowspan=3, sticky="nsw", **Person.padding)

        self.material_tree.bind("<Double-1>", self.fill_material_entries)

        self.populate_existing_materials()

    def populate_existing_materials(self):
        materials = self.db.get_existing_materials()
        self.material_tree.delete(*self.material_tree.get_children())

        for material in materials:
            material_id = material['MaterialID']
            name = f"{material['Name']} {material['Brand']}"
            self.material_tree.insert('', 'end', values=(material_id, name))

    def fill_material_entries(self, event):
        item = self.material_tree.focus()
        if item:
            material_id = self.material_tree.item(item)['values'][0]
            material_info = self.db.get_material_info(material_id)

            def get_valid_string(value):
                return value if isinstance(value, str) else ''

            def get_valid_float(value):
                if isinstance(value, (float, int)):
                    return f"{value:.2f}"
                try:
                    float_value = float(value)
                    return f"{float_value:.2f}"
                except (ValueError, TypeError):
                    return ''

            def get_valid_date(value):
                return value if isinstance(value, (str, datetime.date)) else None

            self.entry_edit_name.delete(0, tk.END)
            self.entry_edit_name.insert(0, get_valid_string(material_info.get('Name', '')))

            self.entry_edit_type.delete(0, tk.END)
            self.entry_edit_type.insert(0, get_valid_string(material_info.get('Type', '')))

            self.entry_edit_brand.delete(0, tk.END)
            self.entry_edit_brand.insert(0, get_valid_string(material_info.get('Brand', '')))

            self.entry_edit_price.delete(0, tk.END)
            self.entry_edit_price.insert(0, get_valid_float(material_info.get('Price', '')))

            # Get the employee ID
            employee_id = material_info.get('EmployeeID', None)

            # Find the employee name from the ID
            employee_name = next((name for name, id in self.edit_employee_options.items() if id == employee_id), '')

            # Set the OptionMenu to the employee name
            self.__edit_selected_employee.set(employee_name)

            start_date = get_valid_date(material_info.get('OpenDate'))
            if start_date:
                self.entry_edit_open_date.set_date(start_date)
            else:
                self.entry_edit_open_date.set_date(datetime.date(1990, 1, 1))

            end_date = get_valid_date(material_info.get('FinishDate'))
            if end_date:
                self.entry_edit_finish_date.set_date(end_date)
            else:
                self.entry_edit_finish_date.set_date(datetime.date(2099, 12, 31))

            self.material_id_to_update = material_id

    def add_material_clicked(self):
        entry_fields = [
            self.entry_name, self.entry_type, self.entry_brand,
            self.entry_price, self.entry_open_date, self.entry_finish_date
        ]
        option_menus = [self.__add_selected_employee]

        values = Person.get_person_data(entry_fields, option_menus)

        try:
            employee_name = self.__add_selected_employee.get()
            employee_id = self.employee_options.get(employee_name, None)
            if employee_id is None:
                raise ValueError("Add employee!")

            values = values[:-1]  # Remove the last element (employee name) from values
            values.append(employee_id)  # Append the employee ID

            Person.check_provided_names(self.entry_name, self.entry_brand)

            self.db.save_material(values)

            Person.clear_input_fields(entry_fields, option_menus)

            self.populate_existing_materials()

            ErrorHandler.show_info("Added", "Successfully added")
        except Exception as e:
            ErrorHandler.show_error("Error", f'Error occured: {e}')

    def edit_material_clicked(self):
        if not self.material_id_to_update:
            ErrorHandler.show_warning("Edit", "Choose material to edit!")
            return

        entry_fields = [
            self.entry_edit_name, self.entry_edit_type, self.entry_edit_brand,
            self.entry_edit_price, self.entry_edit_open_date, self.entry_edit_finish_date
        ]
        option_menus = [self.__edit_selected_employee]

        values = Person.get_person_data(entry_fields, option_menus)

        try:
            employee_name = self.__edit_selected_employee.get()
            employee_id = self.employee_options.get(employee_name, None)
            if employee_id is None:
                raise ValueError("Select employee!")

            values = values[:-1]  # Remove the last element (employee name) from values
            values.append(employee_id)  # Append the employee ID

            Person.check_provided_names(self.entry_name, self.entry_brand)

            self.db.update_material(values, self.material_id_to_update)

            Person.clear_input_fields(entry_fields, option_menus)

            self.populate_existing_materials()

            ErrorHandler.show_info("Edited", "Successfully edited")
        except Exception as e:
            ErrorHandler.show_error("Error", f'Error occured: {e}')

    def search_material(self, event):
        search_term = self.entry_search_material.get().strip().lower()
        self.material_tree.delete(*self.material_tree.get_children())  # Clear existing entries

        if not search_term:
            self.populate_existing_materials()
        else:
            materials = self.db.search_material(search_term)
            for material in materials:
                material_id = material['MaterialID']
                name = f"{material['Name']} {material['Brand']}"
                self.material_tree.insert('', 'end', values=(material_id, name))

    def delete_material_clicked(self):
        if not self.material_id_to_update:
            ErrorHandler.show_warning("Delete", "Choose material to delete!")
            return

        try:
            self.db.delete_material(self.material_id_to_update)
            self.populate_existing_materials()
            ErrorHandler.show_info("Deleted", "Successfully deleted")
            self.material_id_to_update = None
        except Exception as e:
            ErrorHandler.show_error("Error", f"Error occured: {e}")