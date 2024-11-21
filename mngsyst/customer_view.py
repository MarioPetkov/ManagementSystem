import tkinter as tk
from tkinter import ttk, messagebox
from mngsyst.error_handler import ErrorHandler

from person import Person

class CustomerView:
	def __init__(self, notebook, db):
		self.notebook = notebook
		self.db = db
		self.customer_id_to_update = None

		self.frame_customer = ttk.Frame(self.notebook)
		self.frame_customer.configure(height=200, padding=15, width=200)
		self.notebook.add(self.frame_customer, text="Customers")

		self.widgets_add_customer()
		self.widgets_edit_customer()
		self.widgets_customers_list()

	def widgets_add_customer(self):
		self.lblframe_add_customer = ttk.Labelframe(self.frame_customer, text='Add customer')
		self.lblframe_add_customer.configure(height=200, padding=10, width=200)

		self.lbl_f_name = ttk.Label(self.lblframe_add_customer, text='Name*')
		self.lbl_l_name = ttk.Label(self.lblframe_add_customer, text='Surname*')
		self.lbl_phone_num = ttk.Label(self.lblframe_add_customer, text='Phone')
		self.lbl_age = ttk.Label(self.lblframe_add_customer, text='Age')
		self.lbl_city = ttk.Label(self.lblframe_add_customer, text='City')
		self.lbl_ig = ttk.Label(self.lblframe_add_customer, text='Instagram')
		self.lbl_neighborhood = ttk.Label(self.lblframe_add_customer, text='Quarter')
		self.lbl_gender = ttk.Label(self.lblframe_add_customer, text='Sex')

		self.entry_f_name = ttk.Entry(self.lblframe_add_customer)
		self.entry_l_name = ttk.Entry(self.lblframe_add_customer)
		self.entry_phone_num = ttk.Entry(self.lblframe_add_customer)
		self.entry_age = ttk.Entry(self.lblframe_add_customer)
		self.entry_city = ttk.Entry(self.lblframe_add_customer)
		self.entry_ig = ttk.Entry(self.lblframe_add_customer)

		self.__add_selected_neighborhood = tk.StringVar()
		self.optionmenu_neighborhood = ttk.OptionMenu(self.lblframe_add_customer, self.__add_selected_neighborhood,
		                                              None, *Person.neighborhoods)

		self.__add_selected_gender = tk.StringVar(value='Woman')
		self.optionmenu_gender = ttk.OptionMenu(self.lblframe_add_customer, self.__add_selected_gender,
		                                        'Woman',*Person.genders)

		self.btn_add_customer = ttk.Button(self.lblframe_add_customer, text='Add',
		                                   command=self.add_customer_clicked)

		self.lbl_f_name.grid(column=0, row=0, sticky="e", **Person.padding)
		self.lbl_l_name.grid(column=0, row=1, sticky="e", **Person.padding)
		self.lbl_phone_num.grid(column=0, row=2, sticky="e", **Person.padding)
		self.lbl_age.grid(column=0, row=3, sticky="e", **Person.padding)
		self.lbl_city.grid(column=2, row=0, sticky="e", **Person.padding)
		self.lbl_ig.grid(column=2, row=1, sticky="e", **Person.padding)
		self.lbl_neighborhood.grid(column=2, row=2, sticky="e", **Person.padding)
		self.lbl_gender.grid(column=2, row=3, sticky="e", **Person.padding)

		self.entry_f_name.grid(column=1, row=0, sticky="w", **Person.padding)
		self.entry_l_name.grid(column=1, row=1, sticky="w", **Person.padding)
		self.entry_phone_num.grid(column=1, row=2, sticky="w", **Person.padding)
		self.entry_age.grid(column=1, row=3, sticky="w", **Person.padding)
		self.entry_city.grid(column=3, row=0, sticky="w", **Person.padding)
		self.entry_ig.grid(column=3, row=1, sticky="w", **Person.padding)
		self.optionmenu_neighborhood.grid(column=3, row=2, sticky="ew", **Person.padding)
		self.optionmenu_gender.grid(column=3, row=3, sticky="ew", **Person.padding)

		self.btn_add_customer.grid(column=0, columnspan=4, row=4, sticky="ew", **Person.padding)

		self.lblframe_add_customer.grid(column=0, row=0, sticky="nsew", **Person.padding)

	def widgets_edit_customer(self):
		self.lblframe_edit_customer = ttk.Labelframe(self.frame_customer, text='Edit')
		self.lblframe_edit_customer.configure(height=200,padding=10, width=200)

		self.lbl_edit_f_name = ttk.Label(self.lblframe_edit_customer, text='Name*')
		self.lbl_edit_l_name = ttk.Label(self.lblframe_edit_customer, text='Surname*')
		self.lbl_edit_phone_num = ttk.Label(self.lblframe_edit_customer, text='Phone')
		self.lbl_edit_age = ttk.Label(self.lblframe_edit_customer, text='Age')
		self.lbl_edit_city = ttk.Label(self.lblframe_edit_customer, text='City')
		self.lbl_edit_ig = ttk.Label(self.lblframe_edit_customer, text='Instagram')
		self.lbl_edit_neighborhood = ttk.Label(self.lblframe_edit_customer, text='Quarter')
		self.lbl_edit_gender = ttk.Label(self.lblframe_edit_customer, text='Sex')

		self.entry_edit_f_name = ttk.Entry(self.lblframe_edit_customer)
		self.entry_edit_l_name = ttk.Entry(self.lblframe_edit_customer)
		self.entry_edit_phone_num = ttk.Entry(self.lblframe_edit_customer)
		self.entry_edit_age = ttk.Entry(self.lblframe_edit_customer)
		self.entry_edit_city = ttk.Entry(self.lblframe_edit_customer)
		self.entry_edit_ig = ttk.Entry(self.lblframe_edit_customer)

		self.__selected_gender = tk.StringVar()
		self.optionmenu_edit_gender = ttk.OptionMenu(self.lblframe_edit_customer, self.__selected_gender, None,
		                                             *Person.genders)

		self.__selected_neighborhood = tk.StringVar()
		self.optionmenu_edit_neighborhood = ttk.OptionMenu(self.lblframe_edit_customer, self.__selected_neighborhood,
		                                                   None, *Person.neighborhoods)

		self.btn_update_customer = ttk.Button(self.lblframe_edit_customer, text='Edit',
		                                      command=self.edit_customer_clicked)
		self.btn_delete_customer = ttk.Button(self.lblframe_edit_customer, text='Delete',
		                                      command=self.delete_customer_clicked)

		self.lbl_edit_f_name.grid(column=0, row=0, sticky="e", **Person.padding)
		self.lbl_edit_l_name.grid(column=0, row=1, sticky="e", **Person.padding)
		self.lbl_edit_phone_num.grid(column=0, row=2, sticky="e", **Person.padding)
		self.lbl_edit_age.grid(column=0, row=3, sticky="e", **Person.padding)
		self.lbl_edit_city.grid(column=2, row=0, sticky="e", **Person.padding)
		self.lbl_edit_ig.grid(column=2, row=1, sticky="e", **Person.padding)
		self.lbl_edit_neighborhood.grid(column=2, row=2, sticky="e", **Person.padding)
		self.lbl_edit_gender.grid(column=2, row=3, sticky="e", **Person.padding)

		self.entry_edit_f_name.grid(column=1, row=0, sticky="w", **Person.padding)
		self.entry_edit_l_name.grid(column=1, row=1, sticky="w", **Person.padding)
		self.entry_edit_phone_num.grid(column=1, row=2, sticky="w", **Person.padding)
		self.entry_edit_age.grid(column=1, row=3, sticky="w", **Person.padding)
		self.entry_edit_city.grid(column=3, row=0, sticky="w", **Person.padding)
		self.entry_edit_ig.grid(column=3, row=1, sticky="w", **Person.padding)
		self.optionmenu_edit_neighborhood.grid(column=3, row=2, sticky="ew", **Person.padding)
		self.optionmenu_edit_gender.grid(column=3, row=3, sticky="ew", **Person.padding)

		self.btn_update_customer.grid(column=0, columnspan=4, row=4, sticky="ew", **Person.padding)
		self.btn_delete_customer.grid(column=0, columnspan=4, row=5, sticky="ew", **Person.padding)

		self.lblframe_edit_customer.grid(column=0, row=1, sticky="nsew", **Person.padding)

	def widgets_customers_list(self):
		self.lblframe_customers_list = ttk.Labelframe(self.frame_customer, text='Search:')
		self.lblframe_customers_list.configure(height=200, width=200)

		self.customer_tree = ttk.Treeview(self.lblframe_customers_list, columns=('CustomerID', 'Name'), show='headings', height=19)

		self.entry_search_customer = ttk.Entry(self.lblframe_customers_list, width=26)
		self.entry_search_customer.bind("<KeyRelease>", self.search_customers)
		self.entry_search_customer.grid(column=0, row=0, sticky="ew", padx=5, pady=5)

		self.customer_tree.heading('CustomerID', text='№')
		self.customer_tree.heading('Name', text='Customers:')

		self.customer_tree.column('CustomerID', minwidth=0, width=20, stretch=False)
		self.customer_tree.column('Name', minwidth=0, width=100, stretch=True)

		self.scrollbar = tk.Scrollbar(self.lblframe_customers_list, orient="vertical", command=self.customer_tree.yview)
		self.customer_tree.config(yscrollcommand=self.scrollbar.set)

		self.customer_tree.grid(column=0, row=1, sticky="nsew", **Person.padding)
		self.scrollbar.grid(column=1, row=1, sticky="ns", **Person.padding)
		self.lblframe_customers_list.grid(column=1, row=0, rowspan=3, sticky="nsw", **Person.padding)

		self.customer_tree.bind("<Double-1>", self.fill_customer_entries)

		self.populate_existing_customers()

	def populate_existing_customers(self):
		customers = self.db.get_existing_customers()
		self.customer_tree.delete(*self.customer_tree.get_children())

		for customer in customers:
			customer_id = customer['CustomerID']
			name = f"{customer['FirstName']} {customer['LastName']}"
			self.customer_tree.insert('', 'end', values=(customer_id, name))

	def fill_customer_entries(self, event):
		selected = self.customer_tree.focus()
		if selected:
			customer_id = self.customer_tree.item(selected)['values'][0]
			customer_info = self.db.get_customer_info(customer_id)

			# Ensure that the values are valid strings
			def get_valid_string(value):
				return value if isinstance(value, str) else ''

			self.entry_edit_f_name.delete(0, tk.END)
			self.entry_edit_f_name.insert(0, get_valid_string(customer_info.get('FirstName', '')))

			self.entry_edit_l_name.delete(0, tk.END)
			self.entry_edit_l_name.insert(0, get_valid_string(customer_info.get('LastName', '')))

			self.entry_edit_phone_num.delete(0, tk.END)
			self.entry_edit_phone_num.insert(0, get_valid_string(customer_info.get('PhoneNumber', '')))

			self.entry_edit_age.delete(0, tk.END)
			self.entry_edit_age.insert(0, get_valid_string(customer_info.get('Age', '')))

			self.entry_edit_city.delete(0, tk.END)
			self.entry_edit_city.insert(0, get_valid_string(customer_info.get('City', '')))

			self.entry_edit_ig.delete(0, tk.END)
			self.entry_edit_ig.insert(0, get_valid_string(customer_info.get('Instagram', '')))

			self.__selected_neighborhood.set(get_valid_string(customer_info.get('Neighborhood', '')))
			self.__selected_gender.set(get_valid_string(customer_info.get('Gender', '')))
			self.customer_id_to_update = customer_id

	def add_customer_clicked(self):
		entry_fields = [
			self.entry_f_name, self.entry_l_name, self.entry_phone_num,
			self.entry_age, self.entry_city, self.entry_ig
		]
		values = [entry.get() if entry.get() else None for entry in entry_fields]

		neighborhood = self.__add_selected_neighborhood.get() if self.__add_selected_neighborhood.get() else None
		values.append(neighborhood)

		gender = self.__add_selected_gender.get() if self.__add_selected_gender.get() else None
		values.append(gender)
		try:
			self.db.save_customer(values)
			Person.clear_input_fields(entry_fields, [self.__add_selected_neighborhood, self.__add_selected_gender])
			self.populate_existing_customers()
			ErrorHandler.show_info("Added", "Successfully added customer.")
		except Exception as e:
			ErrorHandler.show_error("Error", "Please add first and last name!")

	def edit_customer_clicked(self):
		if not self.customer_id_to_update:
			messagebox.showwarning("Edit", "Choose customer to edit!")
			return

		entry_fields = [
			self.entry_edit_f_name, self.entry_edit_l_name, self.entry_edit_phone_num,
			self.entry_edit_age, self.entry_edit_city, self.entry_edit_ig
		]
		values = [entry.get() if entry.get() else None for entry in entry_fields]

		neighborhood = self.__selected_neighborhood.get() if self.__selected_neighborhood.get() else None
		values.append(neighborhood)

		gender = self.__selected_gender.get() if self.__selected_gender.get() else None
		values.append(gender)

		try:
			self.db.update_customer(values, self.customer_id_to_update)
			Person.clear_input_fields(entry_fields, [self.__selected_neighborhood, self.__selected_gender])
			self.populate_existing_customers()
			ErrorHandler.show_info("Added", "Successfully added customer.")
		except Exception as e:
			ErrorHandler.show_error("Error", "Please add first and last name!")

	def delete_customer_clicked(self):
		if not self.customer_id_to_update:
			ErrorHandler.show_warning("Delete", "Please choose a customer to delete!")
			return

		entry_fields = [
			self.entry_edit_f_name, self.entry_edit_l_name, self.entry_edit_phone_num,
			self.entry_edit_age, self.entry_edit_city, self.entry_edit_ig
		]
		values = [entry.get() if entry.get() else None for entry in entry_fields]

		neighborhood = self.__selected_neighborhood.get() if self.__selected_neighborhood.get() else None
		values.append(neighborhood)

		selected = self.customer_tree.focus()
		if selected:
			self.db.delete_customer(self.customer_id_to_update)
			Person.clear_input_fields(entry_fields, [self.__selected_neighborhood, self.__selected_gender])
			self.populate_existing_customers()
			ErrorHandler.show_info("Deleted", "Successfully deleted employee")

	def search_customers(self, event):
		search_term = self.entry_search_customer.get().strip().lower()
		self.customer_tree.delete(*self.customer_tree.get_children())  # Clear existing entries

		if not search_term:
			# No search term provided, populate with all customers
			self.populate_existing_customers()
		else:
			# Search for customers with matching first name
			customers = self.db.search_customers(search_term)
			for customer in customers:

				customer_id = customer['CustomerID']
				name = f"{customer['FirstName']} {customer['LastName']}"
				self.customer_tree.insert('', 'end', values=(customer_id, name))