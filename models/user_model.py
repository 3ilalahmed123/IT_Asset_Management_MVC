from db import get_db
from collections import OrderedDict #To add RecordOrder field

class User:
    # Get All Users for management menu
    @staticmethod
    def get_all_users():
        db = get_db()
        return db.execute("SELECT * FROM Users").fetchall()

    #Get User details by ID, returns user details as dictionary to add RecordOrder field
    @staticmethod
    def get_user_by_id(user_id):
        db = get_db()
        row = db.execute("SELECT UserID, Forename, Surname, Username, Password, Role FROM Users WHERE UserID = ?", (user_id,)).fetchone()
        if row:
            return OrderedDict([
            ("RecordOrder", "UserID|Forename|Surname|Username|Password|Role"),  # Record Order
            ("UserID", row["UserID"]),
            ("Forename", row["Forename"]),
            ("Surname", row["Surname"]),
            ("Username", row["Username"]),
            ("Password", row["Password"]),
            ("Role", row["Role"])
            ])
        return None
    
    #Create User using the passed in data
    @staticmethod
    def add_user(data):
        db = get_db()
        query = """
            INSERT INTO Users (Forename, Surname, Username, Password, Role)
            VALUES (?, ?, ?, ?, ?)
        """
        db.execute(query, (data['Forename'], data['Surname'], data['Username'], data['Password'], data['Role']))
        db.commit()
        
    #Update User using User ID and passed in data
    @staticmethod
    def update_user(user_id, data):
        db = get_db()
        query = """
            UPDATE Users
            SET UserID = ?, Forename = ?, Surname = ?, Username = ?, Password = ?, Role = ?
            WHERE UserID = ?
        """
        db.execute(
            query,
            (data['UserID'], data['Forename'], data['Surname'], data['Username'], data['Password'], data['Role'], user_id)
        )
        db.commit()

    #Delete User by ID
        @staticmethod
        def delete_user(user_id):
            db = get_db()
            query = "DELETE FROM Users WHERE UserID = ?"
            db.execute(query, (user_id,))
            db.commit()

