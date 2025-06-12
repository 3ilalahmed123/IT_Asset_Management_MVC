from db import get_db
from collections import OrderedDict #To add RecordOrder field

class Loan:
    # Get All Loans for management menu
    @staticmethod
    def get_all_loans():
        db = get_db()
        return db.execute("SELECT * FROM Loans").fetchall()
    
    #Get Loan details by ID, returns loan details as dictionary to add RecordOrder field
    @staticmethod
    def get_loan_by_id(loan_id):
        db = get_db()
        row = db.execute("SELECT * FROM Loans WHERE LoanID = ?", (loan_id,)).fetchone()
        if row:
            return OrderedDict([
            ("RecordOrder", "LoanID|AssetID|UserID|LoanDate|ReturnDate"),  # Record Order
            ("LoanID", row["LoanID"]),
            ("AssetID", row["AssetID"]),
            ("UserID", row["UserID"]),
            ("LoanDate", row["LoanDate"]),
            ("ReturnDate", row["ReturnDate"])
            ])
        return None
    
    #Create Loan using the passed in data
    @staticmethod
    def add_loan(data):
        db = get_db()
        query = """
            INSERT INTO Loans (AssetID, UserID, LoanDate, ReturnDate)
            VALUES (?, ?, ?, ?)
        """
        db.execute(query, (data['AssetID'], data['UserID'], data['LoanDate'], data['ReturnDate']))
        db.commit()

    #Update Loan using Loan ID and passed in data
    @staticmethod
    def update_loan(loan_id, data):
        db = get_db()
        query = """
            UPDATE Loans
            SET LoanID = ?, AssetID = ?, UserID = ?, LoanDate = ?, ReturnDate = ?
            WHERE LoanID = ?
        """
        db.execute(
            query,
            (data['LoanID'], data['AssetID'], data['UserID'], data['LoanDate'], data['ReturnDate'], loan_id)
        )
        db.commit()

#Delete Loan by ID  
    @staticmethod
    def delete_loan(loan_id):
        db = get_db()
        query = "DELETE FROM Loans WHERE LoanID = ?"
        db.execute(query, (loan_id,))
        db.commit()

