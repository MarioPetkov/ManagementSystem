import tkinter as tk
import datetime
from mngsyst.error_handler import ErrorHandler

from tkcalendar import DateEntry


class Person:
    genders = ['Man', 'Woman']
    neighborhoods = ['Gagarin', 'Izgrev', 'Kamenitsa', 'Karshiaka',
                                          'Komatevo', 'Kyuchuka', 'Marasha', 'Proslav',
                                          'Sadiiski', 'Smirnenski', 'Stolipinovo', 'Trakya']
    status = ['Appointed', 'Sucessfull', 'Cancelled']
    padding = {'padx': 2, 'pady': 2}
    @staticmethod
    def get_person_data(entry_fields, option_menus):
        values = []
        for entry in entry_fields:
            if isinstance(entry, DateEntry):
                date_value = entry.get_date()
                values.append(date_value if date_value else None)
            else:
                values.append(entry.get() if entry.get() else None)

        for menu in option_menus:
            values.append(menu.get() if menu.get() else None)

        return values

    @staticmethod
    def clear_input_fields(entry_fields, option_menus):
        for entry in entry_fields:
            entry.delete(0, tk.END)

            if isinstance(entry, DateEntry):
                entry.set_date(None)

        for menu in option_menus:
            menu.set('')

    @staticmethod
    def check_provided_names(first_name, last_name):
        if not first_name.get().strip() and last_name.get().strip():
            ErrorHandler.show_error("Error", "Please add first and last name!")
            return

    def get_valid_string(value):
        return value if isinstance(value, str) else ''

    @staticmethod
    def get_valid_int(value):
        if isinstance(value, int):
            return value
        try:
            int_value = int(value)
            return f"{int_value}"
        except (ValueError, TypeError):
            return ''

    @staticmethod
    def get_valid_date(value):
        return value if isinstance(value, (str, datetime.date)) else None

