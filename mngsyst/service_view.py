from tkinter import ttk, messagebox
import tkinter as tk
from mngsyst.error_handler import ErrorHandler

from person import Person


class ServiceView:
	def __init__(self, notebook, db):
		self.notebook = notebook
		self.db = db
		self.service_id_to_update = None

		self.frame_service = ttk.Frame(self.notebook)
		self.frame_service.configure(height=200, padding=15, width=200)
		self.notebook.add(self.frame_service, text="Services")

		self.widgets_add_service()
		self.widgets_edit_service()
		self.widgets_services_list()

	def widgets_add_service(self):
		self.lblframe_add_service = ttk.Labelframe(self.frame_service, text='Add service')
		self.lblframe_add_service.configure(height=200, padding=10, width=200)

		self.lbl_service_name = ttk.Label(self.lblframe_add_service, text='Service*')
		self.lbl_description = ttk.Label(self.lblframe_add_service, text='Description*')
		self.lbl_duration = ttk.Label(self.lblframe_add_service, text='Duration*')
		self.lbl_price = ttk.Label(self.lblframe_add_service, text='Price*')

		self.entry_service_name = ttk.Entry(self.lblframe_add_service)
		self.entry_description = ttk.Entry(self.lblframe_add_service)
		self.entry_duration = ttk.Entry(self.lblframe_add_service)
		self.entry_price = ttk.Entry(self.lblframe_add_service)

		self.lbl_service_name.grid(column=0, row=0, sticky="e", **Person.padding)
		self.lbl_description.grid(column=0, row=1, sticky="e", **Person.padding)
		self.lbl_duration.grid(column=0, row=2, sticky="e", **Person.padding)
		self.lbl_price.grid(column=0, row=3, sticky="e", **Person.padding)

		self.entry_service_name.grid(column=1, row=0, sticky="e", **Person.padding)
		self.entry_description.grid(column=1, row=1, sticky="e", **Person.padding)
		self.entry_duration.grid(column=1, row=2, sticky="e", **Person.padding)
		self.entry_price.grid(column=1, row=3, sticky="e", **Person.padding)

		self.btn_add_service = ttk.Button(self.lblframe_add_service, text='Add',
		                                  command=self.add_service_clicked)
		self.btn_add_service.grid(column=0, columnspan=2, row=4, sticky="ew", **Person.padding)

		self.lblframe_add_service.grid(column=0, row=0, sticky="nsew", **Person.padding)

	def widgets_edit_service(self):
		self.lblframe_edit_service = ttk.Labelframe(self.frame_service, text='Edit')
		self.lblframe_edit_service.configure(height=200, padding=10, width=200)

		self.lbl_edit_service_name = ttk.Label(self.lblframe_edit_service, text='Serice*')
		self.lbl_edit_description = ttk.Label(self.lblframe_edit_service, text='Description*')
		self.lbl_edit_duration = ttk.Label(self.lblframe_edit_service, text='Duration*')
		self.lbl_edit_price = ttk.Label(self.lblframe_edit_service, text='Price*')

		self.entry_edit_service_name = ttk.Entry(self.lblframe_edit_service)
		self.entry_edit_description = ttk.Entry(self.lblframe_edit_service)
		self.entry_edit_duration = ttk.Entry(self.lblframe_edit_service)
		self.entry_edit_price = ttk.Entry(self.lblframe_edit_service)

		self.lbl_edit_service_name.grid(column=0, row=0, sticky="e", **Person.padding)
		self.lbl_edit_description.grid(column=0, row=1, sticky="e", **Person.padding)
		self.lbl_edit_duration.grid(column=0, row=2, sticky="e", **Person.padding)
		self.lbl_edit_price.grid(column=0, row=3, sticky="e", **Person.padding)

		self.entry_edit_service_name.grid(column=1, row=0, sticky="e", **Person.padding)
		self.entry_edit_description.grid(column=1, row=1, sticky="e", **Person.padding)
		self.entry_edit_duration.grid(column=1, row=2, sticky="e", **Person.padding)
		self.entry_edit_price.grid(column=1, row=3, sticky="e", **Person.padding)

		self.btn_edit_service = ttk.Button(self.lblframe_edit_service, text='Edit',
		                                   command=self.edit_service_clicked)
		self.btn_delete_service = ttk.Button(self.lblframe_edit_service, text='Delete',
		                                     command=self.delete_service_clicked)

		self.btn_edit_service.grid(column=0, columnspan=2, row=4, sticky="ew", **Person.padding)
		self.btn_delete_service.grid(column=0, columnspan=2, row=5, sticky="ew", **Person.padding)

		self.lblframe_edit_service.grid(column=0, row=1, sticky="nsew", **Person.padding)

	def widgets_services_list(self):
		self.lblframe_services_list = ttk.Labelframe(self.frame_service, text='Search:')
		self.lblframe_services_list.configure(height=200, width=200)

		padding = {'padx': 2, 'pady': 2}

		self.service_tree = ttk.Treeview(self.lblframe_services_list, columns=('ServiceID', 'Service Name'), show='headings',
		                                 height=19)

		self.entry_search_service = ttk.Entry(self.lblframe_services_list, width=49)
		self.entry_search_service.bind("<KeyRelease>", self.search_services)
		self.entry_search_service.grid(column=0, row=0, sticky="ew", padx=5, pady=5)

		self.service_tree.heading('ServiceID', text='№')
		self.service_tree.heading('Service Name', text='List of services')

		self.service_tree.column('ServiceID', minwidth=0, width=20, stretch=False)
		self.service_tree.column('Service Name', minwidth=0, width=100, stretch=True)

		self.scrollbar = tk.Scrollbar(self.lblframe_services_list, orient="vertical", command=self.service_tree.yview)
		self.service_tree.config(yscrollcommand=self.scrollbar.set)

		self.service_tree.grid(column=0, row=1, sticky="nsew", **padding)
		self.scrollbar.grid(column=1, row=1, sticky="ns", **padding)
		self.lblframe_services_list.grid(column=2, row=0, rowspan=3, sticky="nsw", **padding)

		self.service_tree.bind("<Double-1>", self.fill_service_entries)

		self.populate_existing_services()

	def fill_service_entries(self, event):
		selected = self.service_tree.focus()
		if selected:
			service_id = self.service_tree.item(selected)['values'][0]
			service_info = self.db.get_service_info(service_id)

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



			self.entry_edit_service_name.delete(0, tk.END)
			self.entry_edit_service_name.insert(0, get_valid_string(service_info.get('ServiceName', '')))

			self.entry_edit_description.delete(0, tk.END)
			self.entry_edit_description.insert(0, get_valid_string(service_info.get('Description', '')))

			self.entry_edit_duration.delete(0, tk.END)
			self.entry_edit_duration.insert(0, Person.get_valid_int(service_info.get('Duration', '')))

			self.entry_edit_price.delete(0, tk.END)
			self.entry_edit_price.insert(0, get_valid_float(service_info.get('Price', '')))

			self.service_id_to_update = service_id

	def populate_existing_services(self):
		services = self.db.get_existing_services()
		self.service_tree.delete(*self.service_tree.get_children())

		for service in services:
			service_id = service['ServiceID']
			service_name = f"{service['ServiceName']}"
			self.service_tree.insert('', 'end', values=(service_id, service_name))

	def add_service_clicked(self):
		entry_fields = [
			self.entry_service_name, self.entry_description,
			self.entry_duration, self.entry_price
		]
		option_menus = []
		values = Person.get_person_data(entry_fields, option_menus)
		try:
			self.db.save_service(values)
			Person.clear_input_fields(entry_fields, option_menus)
			self.populate_existing_services()
			ErrorHandler.show_info("Added", "Successfully added service!")
		except Exception as e:
			ErrorHandler.show_warning("Add", f"Fullfill the mandatory fields")

	def edit_service_clicked(self):
		if not self.service_id_to_update:
			messagebox.showwarning("Edit", "Choose service to edit!")

		entry_fields = [
			self.entry_edit_service_name, self.entry_edit_description,
			self.entry_edit_duration, self.entry_edit_price
		]
		option_menus = []
		values = Person.get_person_data(entry_fields, option_menus)

		try:
			self.db.update_service(values, self.service_id_to_update)
			Person.clear_input_fields(entry_fields, option_menus)
			self.populate_existing_services()
			ErrorHandler.show_info("Edited", "Successfully edited service!")
		except Exception as e:
			ErrorHandler.show_error("Error", f"Error occured: {e}")

	def delete_service_clicked(self):
		if not self.service_id_to_update:
			ErrorHandler.show_warning("Deleted", "Choose service to delete!")

		entry_fields = [
			self.entry_edit_service_name, self.entry_edit_description,
			self.entry_edit_duration, self.entry_edit_price
		]
		option_menus = []

		try:
			self.db.delete_service(self.service_id_to_update)
			Person.clear_input_fields(entry_fields, option_menus)
			self.populate_existing_services()
			ErrorHandler.show_info("Deleted", "Successfully deleted service!")
			self.service_id_to_update = None
		except Exception as e:
			ErrorHandler.show_error("Error", f"Error occured: {e}")

	def search_services(self, event):
		search_term = self.entry_search_service.get().strip().lower()
		self.service_tree.delete(*self.service_tree.get_children())  # Clear existing entries

		if not search_term:
			self.populate_existing_services()
		else:
			services = self.db.search_services(search_term)
			for service in services:
				service_id = service['ServiceID']
				service_name = f"{service['ServiceName']}"
				self.service_tree.insert('', 'end', values=(service_id, service_name))