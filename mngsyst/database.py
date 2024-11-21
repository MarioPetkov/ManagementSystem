import datetime

import psycopg2

from mngsyst.error_handler import ErrorHandler


def get_time_periods():
    today = datetime.date.today()
    last_30_days = today - datetime.timedelta(days=30)
    last_7_days = today - datetime.timedelta(days=7)
    return last_30_days, last_7_days


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self._self_connect_to_db()

    def _self_connect_to_db(self):
        try:
            self.connection = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password='password',
                database='managementsystem'
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            ErrorHandler.show_error("Error",f"Could not connect to the database")
            self._close_connection()

    def _close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def _execute_commit(self, sql, params=()):
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
        except psycopg2.Error as e:
            self.connection.rollback()
            ErrorHandler.show_error("Error",f"Error occured: {e}")
            self._close_connection()
        except Exception as e:
            self.connection.rollback()
            ErrorHandler.show_error("Error",f"Error occured: {e}")
            self._close_connection()

    def __del__(self):
        self._close_connection()

    def _fetch_single(self, sql, params=()):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchone()

    def _fetch_all(self, sql, params=()):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def search_customers(self, search_term):
        search_term = search_term.lower()
        sql = """
        SELECT CustomerID, FirstName, LastName
        FROM Customers
        WHERE LOWER(CONCAT(FirstName, ' ', LastName)) ILIKE %s
        ORDER BY FirstName
        """
        rows = self._fetch_all(sql, (f'%{search_term}%',))
        return [{'CustomerID': row[0], 'FirstName': row[1], 'LastName': row[2]} for row in rows]

    def get_existing_customers(self):
        sql = "SELECT CustomerID, FirstName, LastName FROM Customers ORDER BY FirstName, LastName"
        rows = self._fetch_all(sql)
        return [{'CustomerID': row[0], 'FirstName': row[1], 'LastName': row[2]} for row in rows]

    def get_customer_info(self, customer_id):
        sql = """
        SELECT FirstName, LastName, PhoneNumber, Age, City, Instagram, Neighborhood, Gender 
        FROM Customers WHERE CustomerID = %s
        """
        row = self._fetch_single(sql, (customer_id,))
        if row:
            return {
                'FirstName': row[0],
                'LastName': row[1],
                'PhoneNumber': row[2],
                'Age': row[3],
                'City': row[4],
                'Instagram': row[5],
                'Neighborhood': row[6],
                'Gender': row[7]
            }
        return {}

    def update_customer(self, updated_data, customer_id):
        sql = """
        UPDATE Customers
        SET FirstName = %s, LastName = %s, PhoneNumber = %s, Age = %s,
            City = %s, Instagram = %s, Neighborhood = %s, Gender = %s
        WHERE CustomerID = %s
        """
        self._execute_commit(sql, (*updated_data, customer_id))

    def save_customer(self, values):
        sql = """
        INSERT INTO Customers (FirstName, LastName, PhoneNumber, Age, City, Instagram, Neighborhood, Gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self._execute_commit(sql, values)

    def delete_customer(self, customer_id):
        sql = "DELETE FROM Customers WHERE CustomerID = %s"
        self._execute_commit(sql, (customer_id,))

    def get_customer_appointments(self, customer_id):
        sql = """
        SELECT
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            e.FirstName AS EmployeeFirstName,
            e.LastName AS EmployeeLastName,
            s.ServiceName,
            a.AppointmentDate,
            a.Status,
            s.Price,
            a.Notes
        FROM
            Appointments a
        JOIN
            Employees e ON a.EmployeeID = e.EmployeeID
        JOIN
            Customers c ON a.CustomerID = c.CustomerID
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        WHERE
            a.CustomerID = %s
        ORDER BY
            a.AppointmentDate DESC
        """
        rows = self._fetch_all(sql, (customer_id,))
        return [{'CustomerFirstName': row[0], 'CustomerLastName': row[1], 'EmployeeFirstName': row[2],
                 'EmployeeLastName': row[3], 'ServiceName': row[4], 'AppointmentDate': row[5],
                 'Status': row[6], 'Price': row[7], 'Notes': row[8]} for row in rows]

    def get_customer_money_spent(self, customer_id):
        last_30_days, last_7_days = get_time_periods()

        sql = """
        SELECT
            COALESCE(SUM(CASE WHEN a.Status = 'Sucessfull' THEN s.Price ELSE 0 END), 0) AS total_spent,
            COALESCE(SUM(CASE WHEN a.Status = 'Sucessfull' AND a.AppointmentDate >= %s THEN s.Price ELSE 0 END), 0) AS last_30_days_spent,
            COALESCE(SUM(CASE WHEN a.Status = 'Sucessfull' AND a.AppointmentDate >= %s THEN s.Price ELSE 0 END), 0) AS last_7_days_spent
        FROM
            Appointments a
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        WHERE
            a.CustomerID = %s
        """
        self.cursor.execute(sql, (last_30_days, last_7_days, customer_id))
        row = self.cursor.fetchone()

        return {
            'total_spent': row[0] or 0,
            'last_30_days_spent': row[1] or 0,
            'last_7_days_spent': row[2] or 0
        }

    # Employee methods
    def get_existing_employees(self):
        sql = "SELECT EmployeeID, FirstName, LastName FROM Employees ORDER BY FirstName"
        rows = self._fetch_all(sql)
        return [{'EmployeeID': row[0], 'FirstName': row[1], 'LastName': row[2]} for row in rows]

    def get_employee_info(self, employee_id):
        sql = """
        SELECT FirstName, LastName, PhoneNumber, Age, Position, StartDate, EndDate, Gender 
        FROM Employees WHERE EmployeeID = %s
        """
        row = self._fetch_single(sql, (employee_id,))
        if row:
            return {
                'FirstName': row[0],
                'LastName': row[1],
                'PhoneNumber': row[2],
                'Age': row[3],
                'Position': row[4],
                'StartDate': row[5],
                'EndDate': row[6],
                'Gender': row[7]
            }
        return {}

    def update_employee(self, updated_data, employee_id):
        sql = """
        UPDATE Employees
        SET FirstName = %s, LastName = %s, PhoneNumber = %s, Age = %s,
            Position = %s, StartDate = %s, EndDate = %s, Gender = %s
        WHERE EmployeeID = %s
        """
        self._execute_commit(sql, (*updated_data, employee_id))

    def save_employee(self, values):
        sql = """
        INSERT INTO Employees (FirstName, LastName, PhoneNumber, Age, Position, StartDate, EndDate, Gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self._execute_commit(sql, [None if val == '' else val for val in values])

    def delete_employee(self, employee_id):
        sql = "DELETE FROM Employees WHERE EmployeeID = %s"
        self._execute_commit(sql, (employee_id,))

    def search_employees(self, search_term):
        sql = """
        SELECT EmployeeID, FirstName, LastName
        FROM Employees
        WHERE LOWER(CONCAT(FirstName, ' ', LastName)) ILIKE %s
        ORDER BY FirstName, LastName
        """
        rows = self._fetch_all(sql, (f'%{search_term}%',))
        return [{'EmployeeID': row[0], 'FirstName': row[1], 'LastName': row[2]} for row in rows]

    def get_employee_appointments(self, employee_id):
        sql = """
        SELECT
            e.FirstName AS EmployeeFirstName,
            e.LastName AS EmployeeLastName,
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            s.ServiceName,
            a.AppointmentDate,
            a.Status,
            a.Notes
        FROM
            Appointments a
        JOIN
            Employees e ON a.EmployeeID = e.EmployeeID
        JOIN
            Customers c ON a.CustomerID = c.CustomerID
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        WHERE
            e.EmployeeID = %s
        ORDER BY
            a.AppointmentDate DESC
        """
        rows = self._fetch_all(sql, (employee_id,))
        return [{'EmployeeFirstName': row[0], 'EmployeeLastName': row[1], 'CustomerFirstName': row[2],
                 'CustomerLastName': row[3], 'ServiceName': row[4], 'AppointmentDate': row[5],
                 'Status': row[6], 'Notes': row[7]} for row in rows]

    def get_employee_earnings(self, employee_id):
        sql = """
        SELECT
            SUM(CASE WHEN a.Status = 'Sucessfull' THEN s.Price ELSE 0 END) AS total_earnings,
            SUM(CASE WHEN a.Status = 'Sucessfull' AND a.AppointmentDate >= NOW() - INTERVAL '30 days' THEN s.Price ELSE 0 END) AS last_30_days_earnings,
            SUM(CASE WHEN a.Status = 'Sucessfull' AND a.AppointmentDate >= NOW() - INTERVAL '7 days' THEN s.Price ELSE 0 END) AS last_7_days_earnings
        FROM
            Appointments a
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        WHERE
            a.EmployeeID = %s
        """
        row = self._fetch_single(sql, (employee_id,))
        return {
            'total_earnings': row[0] or 0,
            'last_30_days_earnings': row[1] or 0,
            'last_7_days_earnings': row[2] or 0
        }

    def get_money_invested(self, employee_id):
        last_30_days, last_7_days = get_time_periods()

        sql = """
            SELECT
                COALESCE(SUM(m.Price), 0) AS total_spent,
                COALESCE(SUM(CASE WHEN a.AppointmentDate >= %s THEN m.Price ELSE 0 END), 0) AS last_30_days_spent,
                COALESCE(SUM(CASE WHEN a.AppointmentDate >= %s THEN m.Price ELSE 0 END), 0) AS last_7_days_spent
            FROM
                Appointments a
            JOIN
                Employees e ON a.EmployeeID = e.EmployeeID
            JOIN
                Materials m ON a.EmployeeID = e.EmployeeID
            WHERE
                a.EmployeeID = %s
                AND a.Status = 'Sucessfull'
            """
        row = self._fetch_single(sql, (last_30_days, last_7_days, employee_id))
        return {
            'total_spent': row[0] or 0,
            'last_30_days_spent': row[1] or 0,
            'last_7_days_spent': row[2] or 0
        }

    # Service methods
    def get_existing_services(self):
        sql = "SELECT ServiceID, ServiceName FROM Services ORDER BY ServiceName"
        rows = self._fetch_all(sql)
        return [{'ServiceID': row[0], 'ServiceName': row[1]} for row in rows]

    def get_service_info(self, service_id):
        sql = """
        SELECT ServiceName, Description, Duration, Price
        FROM Services
        WHERE ServiceID = %s
        """
        row = self._fetch_single(sql, (service_id,))
        if row:
            return {
                'ServiceName': row[0],
                'Description': row[1],
                'Duration': row[2],
                'Price': row[3]
            }
        return {}

    def save_service(self, values):
        sql = """
        INSERT INTO Services (ServiceName, Description, Duration, Price)
        VALUES (%s, %s, %s, %s)
        """
        self._execute_commit(sql, values)

    def update_service(self, updated_data, service_id):
        sql = """
        UPDATE Services
        SET ServiceName = %s, Description = %s, Duration = %s, Price = %s
        WHERE ServiceID = %s
        """
        self._execute_commit(sql, (*updated_data, service_id))

    def delete_service(self, service_id):
        sql = "DELETE FROM Services WHERE ServiceID = %s"
        self._execute_commit(sql, (service_id,))

    def search_services(self, search_term):
        sql = """
        SELECT ServiceID, ServiceName
        FROM Services
        WHERE LOWER(ServiceName) ILIKE %s
        """
        rows = self._fetch_all(sql, (f'%{search_term}%',))
        return [{'ServiceID': row[0], 'ServiceName': row[1]} for row in rows]

    # Material methods
    def get_existing_materials(self):
        sql = "SELECT MaterialID, Name, Brand FROM Materials ORDER BY Name"
        rows = self._fetch_all(sql)
        return [{'MaterialID': row[0], 'Name': row[1], 'Brand': row[2]} for row in rows]

    def get_material_info(self, material_id):
        sql = """
        SELECT Name, Type, Brand, Price, OpenDate, FinishDate, EmployeeID
        FROM Materials
        WHERE MaterialID = %s
        """
        row = self._fetch_single(sql, (material_id,))
        if row:
            return {
                'Name': row[0],
                'Type': row[1],
                'Brand': row[2],
                'Price': row[3],
                'OpenDate': row[4],
                'FinishDate': row[5],
                'EmployeeID': row[6]
            }
        return {}

    def save_material(self, values):
        sql = """
        INSERT INTO Materials (Name, Type, Brand, Price, OpenDate, FinishDate, EmployeeID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self._execute_commit(sql, [None if val == '' else val for val in values])

    def update_material(self, updated_data, material_id):
        sql = """
        UPDATE Materials
        SET Name = %s, Type = %s, Brand = %s, Price = %s, OpenDate = %s, FinishDate = %s, EmployeeID = %s
        WHERE MaterialID = %s
        """
        self._execute_commit(sql, (*updated_data, material_id))

    def delete_material(self, material_id):
        sql = "DELETE FROM Materials WHERE MaterialID = %s"
        self._execute_commit(sql, (material_id,))

    def search_material(self, search_term):
        sql = """
        SELECT MaterialID, Name, Brand
        FROM Materials
        WHERE LOWER(CONCAT(Name, ' ', Brand)) ILIKE %s
        """
        rows = self._fetch_all(sql, (f'%{search_term}%',))
        return [{'MaterialID': row[0], 'Name': row[1], 'Brand': row[2]} for row in rows]

    # Appointment methods
    def save_appointment(self, employee_id, customer_id, service_id, appointment_date, status, notes):
        sql = """
        INSERT INTO Appointments (EmployeeID, CustomerID, ServiceID, AppointmentDate, Status, Notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self._execute_commit(sql, (employee_id, customer_id, service_id, appointment_date, status, notes))

    def update_appointment(self, appointment_id, employee_id, customer_id, service_id, appointment_date, status, notes):
        sql = """
        UPDATE Appointments
        SET EmployeeID = %s, CustomerID = %s, ServiceID = %s, AppointmentDate = %s, Status = %s, Notes = %s
        WHERE AppointmentID = %s
        """
        self._execute_commit(sql, (employee_id, customer_id, service_id, appointment_date, status, notes, appointment_id))

    def delete_appointment(self, appointment_id):
        sql = "DELETE FROM Appointments WHERE AppointmentID = %s"
        self._execute_commit(sql, (appointment_id,))

    def get_existing_appointments(self):
        sql = """
        SELECT
            a.AppointmentID,
            e.FirstName AS EmployeeFirstName,
            e.LastName AS EmployeeLastName,
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            s.ServiceName,
            a.AppointmentDate,
            a.Status,
            a.Notes
        FROM
            Appointments a
        JOIN
            Employees e ON a.EmployeeID = e.EmployeeID
        JOIN
            Customers c ON a.CustomerID = c.CustomerID
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        ORDER BY a.AppointmentDate DESC
        """
        rows = self._fetch_all(sql)
        return [
            {
                'AppointmentID': row[0],
                'EmployeeFirstName': row[1],
                'EmployeeLastName': row[2],
                'CustomerFirstName': row[3],
                'CustomerLastName': row[4],
                'ServiceName': row[5],
                'AppointmentDate': row[6].strftime('%Y-%m-%d'),
                'Status': row[7],
                'Notes': row[8]
            }
            for row in rows
        ]

    def search_appointments(self, search_term):
        search_terms = search_term.lower().split()

        sql = """
        SELECT
            a.AppointmentID,
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            e.FirstName AS EmployeeFirstName,
            e.LastName AS EmployeeLastName,
            s.ServiceName,
            a.AppointmentDate,
            a.Status,
            s.Price,
            a.Notes
        FROM
            Appointments a
        JOIN
            Customers c ON a.CustomerID = c.CustomerID
        JOIN
            Employees e ON a.EmployeeID = e.EmployeeID
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        WHERE
        """

        conditions = []
        params = []

        for term in search_terms:
            like_clause = """
            LOWER(c.FirstName) ILIKE %s OR LOWER(c.LastName) ILIKE %s OR 
            LOWER(e.FirstName) ILIKE %s OR LOWER(e.LastName) ILIKE %s OR 
            LOWER(s.ServiceName) ILIKE %s OR LOWER(a.Status) ILIKE %s
            """
            conditions.append(f"({like_clause})")
            params.extend([f"%{term}%"] * 6)  # Use the term for all relevant fields

        sql += " AND ".join(conditions)  # Combine all conditions with AND
        sql += " ORDER BY a.AppointmentDate DESC"  # Sort results by appointment date

        rows = self._fetch_all(sql, tuple(params))

        return [{'AppointmentID': row[0], 'CustomerFirstName': row[1], 'CustomerLastName': row[2],
                 'EmployeeFirstName': row[3], 'EmployeeLastName': row[4], 'ServiceName': row[5],
                 'AppointmentDate': row[6], 'Status': row[7], 'Price': row[8], 'Notes': row[9]} for row in rows]

    def fetch_appointment_by_id(self, appointment_id):
        sql = """
        SELECT
            a.AppointmentID,
            e.FirstName AS EmployeeFirstName,
            e.LastName AS EmployeeLastName,
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            s.ServiceName,
            a.AppointmentDate,
            a.Status,
            a.Notes
        FROM
            Appointments a
        JOIN
            Employees e ON a.EmployeeID = e.EmployeeID
        JOIN
            Customers c ON a.CustomerID = c.CustomerID
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        WHERE
            a.AppointmentID = %s
        """
        row = self._fetch_single(sql, (appointment_id,))
        if row:
            return {
                'AppointmentID': row[0],
                'EmployeeFirstName': row[1],
                'EmployeeLastName': row[2],
                'CustomerFirstName': row[3],
                'CustomerLastName': row[4],
                'ServiceName': row[5],
                'AppointmentDate': row[6].strftime('%Y-%m-%d'),
                'Status': row[7],
                'Notes': row[8]
            }
        return {}

    def get_past_scheduled_appointments(self):
        today = datetime.date.today()
        sql = """
        SELECT
            a.AppointmentID,
            e.FirstName AS EmployeeFirstName,
            e.LastName AS EmployeeLastName,
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            s.ServiceName,
            a.AppointmentDate,
            a.Status,
            a.Notes
        FROM
            Appointments a
        JOIN
            Employees e ON a.EmployeeID = e.EmployeeID
        JOIN
            Customers c ON a.CustomerID = c.CustomerID
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        WHERE
            a.AppointmentDate < %s AND a.Status = 'Записан'
        ORDER BY
            a.AppointmentDate DESC
        """
        rows = self._fetch_all(sql, (today,))
        return [
            {
                'AppointmentID': row[0],
                'EmployeeFirstName': row[1],
                'EmployeeLastName': row[2],
                'CustomerFirstName': row[3],
                'CustomerLastName': row[4],
                'ServiceName': row[5],
                'AppointmentDate': row[6].strftime('%Y-%m-%d'),
                'Status': row[7],
                'Notes': row[8]
            }
            for row in rows
        ]

    def update_appointment_status(self, appointment_id, new_status):
        sql = """
        UPDATE Appointments
        SET Status = %s
        WHERE AppointmentID = %s
        """
        self._execute_commit(sql, (new_status, appointment_id))

    def get_customer_appointment_counts(self, customer_id):
        sql = """
        SELECT
            COUNT(*) AS total_appointments,
            COUNT(*) FILTER (WHERE a.AppointmentDate >= %s) AS last_30_days_appointments,
            COUNT(*) FILTER (WHERE a.AppointmentDate >= %s) AS last_7_days_appointments
        FROM
            Appointments a
        WHERE
            a.CustomerID = %s
        """

        last_30_days, last_7_days = get_time_periods()
        params = (last_30_days, last_7_days, customer_id)

        result = self._fetch_single(sql, params)

        return {
            'total_appointments': result[0],
            'last_30_days_appointments': result[1],
            'last_7_days_appointments': result[2]
        }

    def count_appointments_summary(self, search_terms=None):
        last_30_days, last_7_days = get_time_periods()

        # Base SQL query for counting appointments with joins
        base_sql = """
        SELECT
            COUNT(*) AS total_count,
            COUNT(*) FILTER (WHERE a.AppointmentDate >= %s) AS last_30_days_count,
            COUNT(*) FILTER (WHERE a.AppointmentDate >= %s) AS last_7_days_count
        FROM Appointments a
        JOIN Employees e ON a.EmployeeID = e.EmployeeID
        JOIN Customers c ON a.CustomerID = c.CustomerID
        JOIN Services s ON a.ServiceID = s.ServiceID
        """

        params = [last_30_days, last_7_days]

        # Modify the SQL query if search terms are provided
        if search_terms:
            like_clause = " AND ".join([
                f"(e.FirstName ILIKE %s OR e.LastName ILIKE %s OR c.FirstName ILIKE %s OR c.LastName ILIKE %s OR s.ServiceName ILIKE %s)"
                for _ in search_terms
            ])
            base_sql += " WHERE " + like_clause

            # Add search terms to params (each term is repeated 5 times for the placeholders)
            search_values = [f"%{term}%" for term in search_terms for _ in range(5)]
            params.extend(search_values)

        # Execute the query and fetch the result
        result = self._fetch_single(base_sql, tuple(params))

        return {
            'total_count': result[0],
            'last_30_days_count': result[1],
            'last_7_days_count': result[2]
        }

    def fetch_all_appointments_ordered(self, order_by='AppointmentDate', ascending=True):
        order_direction = 'DESC' if ascending else 'ASCe'
        sql = f"""
        SELECT
            a.AppointmentID,
            e.FirstName AS EmployeeFirstName,
            e.LastName AS EmployeeLastName,
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            s.ServiceName,
            a.AppointmentDate,
            a.Status,
            a.Notes
        FROM
            Appointments a
        JOIN
            Employees e ON a.EmployeeID = e.EmployeeID
        JOIN
            Customers c ON a.CustomerID = c.CustomerID
        JOIN
            Services s ON a.ServiceID = s.ServiceID
        ORDER BY {order_by} {order_direction}
        """
        rows = self._fetch_all(sql)
        return [
            {
                'AppointmentID': row[0],
                'EmployeeFirstName': row[1],
                'EmployeeLastName': row[2],
                'CustomerFirstName': row[3],
                'CustomerLastName': row[4],
                'ServiceName': row[5],
                'AppointmentDate': row[6].strftime('%Y-%m-%d'),
                'Status': row[7],
                'Notes': row[8]
            }
            for row in rows
        ]