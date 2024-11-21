# Business Management Desktop Application

A **Python-based desktop application** designed for business owners to streamline their operations. The application enables scheduling and managing employee appointments, tracking customer interactions, and generating insightful statistics to improve business decisions.

---

## Features

- **Appointment Scheduling:**  
  Efficiently manage employee and customer appointments with an intuitive interface.

- **Customer Management:**  
  Keep detailed records of customers, including demographics and activity statistics.

- **Employee Tracking:**  
  Maintain employee information and appointment assignments.

- **Service Management:**  
  Manage and customize the services offered, their durations, and pricing.

- **Statistics and Reporting:**  
  Generate and view reports on customer interactions, employee performance, and financial statistics.

---

## Screenshots
<img width="920" alt="Screenshot 2024-11-21 at 13 14 04" src="https://github.com/user-attachments/assets/5fc4762b-74f3-41e8-88ce-e2240d42c92f">
<img width="920" alt="Screenshot 2024-11-21 at 13 18 26" src="https://github.com/user-attachments/assets/dc6b28f8-0c99-4db7-8cea-f273e6b4de29">
<img width="920" alt="Screenshot 2024-11-21 at 13 23 52" src="https://github.com/user-attachments/assets/7ec4dbcc-de5f-4197-a764-b9c6eea27005">
<img width="920" alt="Screenshot 2024-11-21 at 13 26 04" src="https://github.com/user-attachments/assets/f9ab55e8-e9ca-4a66-b224-179996ecd490">
<img width="920" alt="Screenshot 2024-11-21 at 13 27 24" src="https://github.com/user-attachments/assets/ea795c8e-c7c1-4055-a89f-19080e41966c">
<img width="920" alt="Screenshot 2024-11-21 at 13 28 08" src="https://github.com/user-attachments/assets/56f6db20-8fe1-4f7d-86d3-9f61c7dd6ca1">
<img width="920" alt="Screenshot 2024-11-21 at 13 28 23" src="https://github.com/user-attachments/assets/6a44f0d3-b16c-4f57-a42f-3babdc956236">
<img width="920" alt="Screenshot 2024-11-21 at 13 30 12" src="https://github.com/user-attachments/assets/d948db9f-093d-4df1-952e-a6d596011a5f">
<img width="920" alt="Screenshot 2024-11-21 at 13 30 20" src="https://github.com/user-attachments/assets/7390a07f-fb25-4a5b-9d74-9484f855517d">
<img width="920" alt="Screenshot 2024-11-21 at 13 30 30" src="https://github.com/user-attachments/assets/1fa53530-f2dc-4e4f-ba97-deaa61301877">
<img width="920" alt="Screenshot 2024-11-21 at 13 30 53" src="https://github.com/user-attachments/assets/6e187c36-f062-4021-acb0-3900a88b557c">
<img width="920" alt="Screenshot 2024-11-21 at 13 31 43" src="https://github.com/user-attachments/assets/bbc97477-9637-45c9-81f6-17943ae1c356">

---

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL Database

---

### Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/MarioPetkov/ManagementSystem.git
   cd ManagementSystem
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up the database:

  * Create the database in PostgreSQL.
  * Run the SQL scripts to create the required tables.

4. Run the application:
   ```bash
   python main.py

---

### Database Setup

To set up the database, follow these steps:

1. Open your PostgreSQL client or connect via a terminal.
2. Create a new database:
   ```sql
   CREATE DATABASE ManagementSystem;
3. Run the create_db.sql script to create the tables:
   ```bash
   psql -U postgres -d managementsystem -f create_db.sql


---

## Technologies Used
- **Python: Backend logic and desktop interface.**
- **Tkinter: User Interface.**
- **PostgreSQL: Database for storing all records.**
- **psycopg2: PostgreSQL driver for Python.**
- **tkcalendar: Date picker functionality.**

---

## Future Enhancements
- **Improve error handling.**
- **Add multi-language support..**
- **Implement email notifications for appointments..**
- **Enhance reporting with visual charts..**

---

## Contributing
Contributions are welcome!
Feel free to fork the repository and submit a pull request with your changes.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For questions or feedback, feel free to reach out at:
- **Email: mariopetkov01@gmail.com**
- **GitHub: github.com/MarioPetkov**
