-- Users Table
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Forename TEXT NOT NULL,
    Surname TEXT NOT NULL,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Role TEXT CHECK(Role IN ('Admin', 'Regular')) NOT NULL
);


-- Assets Table
CREATE TABLE Assets (
    AssetID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Type TEXT NOT NULL,
    Status TEXT CHECK(Status IN ('Unassigned', 'Assigned', 'Service/Repair')) NOT NULL
);

-- Loans Table
CREATE TABLE Loans (
    LoanID INTEGER PRIMARY KEY AUTOINCREMENT,
    AssetID INTEGER NOT NULL, -- Foreign key to Assets
    UserID INTEGER NOT NULL, -- Foreign key to Users
    LoanDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (AssetID) REFERENCES Assets(AssetID) ON DELETE CASCADE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Test Data 10 records per table 

-- Users
-- Insert Test Admins
INSERT INTO Users (Forename, Surname, Username, Password, Role)
VALUES 
('Test', 'Admin1', 'admin1', 'password123', 'Admin'),
('Test', 'Admin2', 'admin2', 'password123', 'Admin');

-- Insert Test Users
INSERT INTO Users (Forename, Surname, Username, Password, Role)
VALUES 
('Test', 'User1', 'user1', 'password123', 'Regular'),
('Test', 'User2', 'user2', 'password123', 'Regular'),
('Alice', 'Smith', 'alice', 'password123', 'Regular'),
('Bob', 'Jones', 'bob', 'password123', 'Regular'),
('Charlie', 'Brown', 'charlie', 'password123', 'Regular'),
('Dave', 'Clark', 'dave', 'password123', 'Regular'),
('Eve', 'Adams', 'eve', 'password123', 'Regular'),
('Grace', 'Miller', 'grace', 'password123', 'Regular');


--Assets
-- Insert Assigned Assets
INSERT INTO Assets (Name, Type, Status)
VALUES 
('Workstation', 'Electronics', 'Assigned'),
('Tablet', 'Electronics', 'Assigned'),
('Desktop Computer', 'Electronics', 'Assigned'),
('Projector', 'Office Equipment', 'Assigned'),
('Smartphone', 'Electronics', 'Assigned');

-- Insert Unassigned Assets
INSERT INTO Assets (Name, Type, Status)
VALUES 
('Laptop', 'Electronics', 'Unassigned'),
('Monitor', 'Electronics', 'Unassigned'),
('Keyboard', 'Electronics', 'Unassigned'),
('Printer', 'Peripherals', 'Unassigned'),
('Desk Phone', 'Office Equipment', 'Unassigned');

-- Loans
-- Insert Loans for Assigned Assets
INSERT INTO Loans (AssetID, UserID, LoanDate, ReturnDate)
VALUES 
(6, 1, '2024-11-01', NULL), -- Workstation loaned to user1
(7, 2, '2024-11-01', NULL), -- Tablet loaned to user2
(8, 3, '2024-11-05', NULL), -- Desktop Computer loaned to alice
(9, 4, '2024-11-07', '2024-11-15'), -- Projector returned by bob
(10, 5, '2024-11-10', NULL), -- Smartphone loaned to charlie
(6, 6, '2024-10-15', '2024-10-30'), -- Workstation returned by dave
(7, 7, '2024-09-20', NULL), -- Tablet loaned to eve
(8, 8, '2024-11-08', NULL), -- Desktop Computer loaned to grace
(9, 5, '2024-11-11', '2024-11-18'), -- Projector returned by charlie
(10, 4, '2024-11-01', NULL); -- Smartphone loaned to bob