CREATE TABLE Customers (
    CustomerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(30) NOT NULL,
    LastName VARCHAR(30) NOT NULL,
    PhoneNumber VARCHAR(10) NULL,
    Age INTEGER NULL,
    City VARCHAR(20) NULL,
    Instagram VARCHAR(30) NULL,
    Neighborhood VARCHAR(20) NULL CHECK (Neighborhood in
                                         ('Gagarin', 'Izgrev', 'Kamenitsa', 'Karshiaka',
                                          'Komatevo', 'Kyuchuka', 'Marasha', 'Proslav',
                                          'Sadiiski', 'Smirnenski', 'Stolipinovo', 'Trakya')),
    Gender VARCHAR(10) NULL CHECK (Gender in ('Man', 'Woman')),
    CONSTRAINT check_phone_number_customers
    CHECK (PhoneNumber ~ '^[0-9]{10}$')
);

CREATE TABLE Employees (
    EmployeeID SERIAL PRIMARY KEY,
    FirstName VARCHAR(30) NOT NULL,
    LastName VARCHAR(30) NOT NULL,
    PhoneNumber VARCHAR(10) NULL,
    Position VARCHAR(20) NULL,
    Age INTEGER NULL,
    StartDate DATE NOT NULL DEFAULT CURRENT_DATE,
    EndDate DATE NULL,
    Gender VARCHAR(10) NULL CHECK (Gender in ('Man', 'Woman')),
    CONSTRAINT check_phone_number_employees
    CHECK (PhoneNumber ~ '^[0-9]{10}$')
);

CREATE TABLE Services (
    ServiceID SERIAL PRIMARY KEY,
    ServiceName VARCHAR(30) NOT NULL,
    Description TEXT NOT NULL,
    Duration INTEGER NOT NULL,
    Price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Materials (
    MaterialID SERIAL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    Type VARCHAR(30),
    Brand VARCHAR(30),
    Price DECIMAL(10, 2),
    OpenDate DATE NOT NULL DEFAULT CURRENT_DATE,
    FinishDate DATE,
    EmployeeID INTEGER NOT NULL,
    FOREIGN KEY (EmployeeID)
        REFERENCES Employees(EmployeeID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Appointments (
    AppointmentID SERIAL PRIMARY KEY,
    EmployeeID INTEGER NOT NULL,
    CustomerID INTEGER NOT NULL,
    ServiceID INTEGER NOT NULL,
    AppointmentDate DATE NOT NULL DEFAULT CURRENT_DATE,
    Status VARCHAR(20) NOT NULL CHECK (
        Status IN ('Appointed', 'Sucessfull', 'Cancelled')),
    Notes TEXT,
    FOREIGN KEY (EmployeeID)
        REFERENCES Employees(EmployeeID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (ServiceID)
        REFERENCES Services(ServiceID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);